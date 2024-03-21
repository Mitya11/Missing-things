from difflib import SequenceMatcher
import scipy
from MessageHandler import MessageHandler

def scoring(source, target):

    levenstein_distance = SequenceMatcher(None, source["object"], target["object"]).ratio()
    if not target["object_vector"] is None and not source["object_vector"] is None:
        similarity = 1 -scipy.spatial.distance.cosine(source["object_vector"],target["object_vector"])
    else:
        similarity = 0
    if not target["features_vector"] is None and not source["features_vector"] is None:
        feature_similarity = 1 - scipy.spatial.distance.cosine(source["features_vector"],target["features_vector"])
    else:
        feature_similarity = 0
    if not target["features_vector"] is None and not source["object_vector"] is None:
        feature_to_obj_similariry = 1 - scipy.spatial.distance.cosine(source["object_vector"],target["features_vector"])
    else:
        feature_to_obj_similariry = 0
    score = max(levenstein_distance,similarity) + 0.5*feature_similarity + 0.5 * feature_to_obj_similariry
    return score
