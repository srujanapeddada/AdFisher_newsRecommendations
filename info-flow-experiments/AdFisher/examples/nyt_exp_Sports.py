import sys, os
sys.path.append("../core")          # files from the core 
import adfisher                     # adfisher wrapper function
import web.pre_experiment.alexa     # collecting top sites from alexa
import web.nytimes_news              # interacting with Google News
import converter.reader             # read log and create feature vectors
import analysis.statistics          # statistics for significance testing

log_file = 'log.nyt_searchAndClick_Sports.txt'
site_file = 'substance.txt'
control_file = 'ControlSites.txt'

def make_browser(unit_id, treatment_id):
    b = web.nytimes_news.NYTNewsUnit(browser='firefox', log_file=log_file, unit_id=unit_id, 
        treatment_id=treatment_id, headless=False, proxy = None)
    return b

#web.pre_experiment.alexa.collect_sites(make_browser, num_sites=5, output_file=site_file,
#    alexa_link="http://www.alexa.com/topsites")

# Control Group treatment
def control_treatment(unit):
    pass

# Experimental Group treatment
def exp_treatment(unit):
    unit.read_NYT_articles(count=5, keyword='a', category='Sports', time_on_site=20)
    unit.read_NYT_articles(count=5, keyword='in', category='Sports', time_on_site=20)
    unit.read_NYT_articles(count=5, keyword='to', category='Sports', time_on_site=20)


# Measurement - Collects ads
def measurement(unit):
    unit.get_recommendedStories()


# Shuts down the browser once we are done with it.
def cleanup_browser(unit):
    unit.quit()

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

# Load results reads the log_file, and creates feature vectors
def load_results():
    collection, names = converter.reader.read_log(log_file)
    return converter.reader.get_feature_vectors(collection, feat_choice='news')

def test_stat(observed_values, unit_assignments):
    return analysis.statistics.difference(observed_values, unit_assignments)


adfisher.do_experiment(make_unit=make_browser, treatments=[control_treatment, exp_treatment], 
                        measurement=measurement, end_unit=cleanup_browser,
                        load_results=load_results, test_stat=test_stat, ml_analysis=True, 
                        num_blocks=25, num_units=4, timeout=2000,
                        log_file=log_file, exp_flag=True, analysis_flag=True, 
                        treatment_names=["control", "experimental"])

