from user_requests import SbI_list, SbT_list, vQA_list, eGeos_list, chat_list
import spacy
import en_core_web_sm
from sklearn.metrics.pairwise import cosine_similarity
import random
import string
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('bert-base-nli-mean-tokens')

SbI_embeddings = model.encode(SbI_list)
vQA_embeddings = model.encode(vQA_list)
eGeos_embeddings = model.encode(eGeos_list)
SbT_embeddings = model.encode(SbT_list)
chat_embeddings = model.encode(chat_list)

nlp = en_core_web_sm.load()


def user_input_format(user_input):
    if user_input['image'] != '':
        if user_input['text'] == '':
            return 'image'
        else:
            return 'text + image'
    if user_input['text'] != '':
        return 'text'


def engine_selection_2a(text):
    text_embeddings = [model.encode(text)]
    max_similarities = ([cosine_similarity(text_embeddings, SbI_embeddings[:]).max(),
                         cosine_similarity(text_embeddings, vQA_embeddings[:]).max(),
                         cosine_similarity(text_embeddings, eGeos_embeddings[:]).max()])
    return ['SbI', 'vQA', 'eGeos'][max_similarities.index(max(max_similarities))]


def SbT_activation(text):
    activation = False
    # find users request's embedding
    text_embeddings = [model.encode(text)]
    print(cosine_similarity(text_embeddings, SbT_embeddings[:]).max())
    if 0.4 < cosine_similarity(text_embeddings, SbT_embeddings[:]).max():
      activation = True
    
    return activation
    
def conversational_activation(text):
    # only activated if the case is a very basic dialog utterance, eg. 'thank you!'
    activation = False
    # find users request's embedding
    text_embeddings = [model.encode(text)]
    if 0.9 < cosine_similarity(text_embeddings, chat_embeddings[:]).max():
      print(cosine_similarity(text_embeddings, chat_embeddings[:]).max())
      activation = True
    
    return activation

def request_disambiguation(text):
    disambiguation = {'need': False,
                      'message': ''}
    if ' near ' in text or ',near ' in text:
        disambiguation['need'] = True
        disambiguation['message'] = "Can you repeat your question replacing 'near' with a specific distance, please?"

    return disambiguation


def existence_of_geographical_object(textual_input):
  geo_object_presense = False
  nlp = en_core_web_sm.load()
  doc = nlp(textual_input)

  geographical_objects = []
  for X in doc.ents:
    if X.label_ in ['GPE','FAC','LOC']:
      geographical_objects.append(X)

    # hacked ORG, must work on it
    if X.label_ == 'ORG':
      doc2 = 'near '+ str(X)
      geographical_objects.append(X)

  if len(geographical_objects)>0:
    geo_object_presense = True

  return [geo_object_presense,geographical_objects]




def earthQA_activation(text):
  activation = existence_of_geographical_object(text)[0]
  return activation


def get_pps(text): # prepositional parts
  nlp = en_core_web_sm.load()
  doc = nlp(text)
  pps = []
  for token in doc:
      if token.pos_ == 'ADP':
          pp = ' '.join([tok.orth_ for tok in token.subtree])
          pps.append(pp)
  return pps
  
def distance_prep_phrase(textual_input):
  distance_phrase = []
  nlp = en_core_web_sm.load()
  doc = nlp(textual_input)
    
  distance_entities = []
  for X in doc.ents:
    if X.label_=='QUANTITY':
        distance_entities.append(X)
    
  if distance_entities == []:
      return distance_phrase
        
  pps =[]      
  for token in doc:
    if token.pos_ == 'ADP':
        pp = ' '.join([tok.orth_ for tok in token.subtree])
        if str(distance_entities[0]) in pp:
          pps.append(pp)
  return pps

def complex_request_decompose(text):
  prepositional_phrases = get_pps(text)
  output_to_earthQA = []
  output_to_SbT = text

  for geo_object in existence_of_geographical_object(text)[1]:
    pps_containing_object = []
    for pp in prepositional_phrases:
      if str(geo_object) in pp:
        pps_containing_object.append(pp)
    
    output_to_earthQA.append(min(pps_containing_object, key = len))


  dpp_out_earthQA = []
  for i,oeQA in enumerate(output_to_earthQA):
    dpp_earthQA = []
    for dpp in distance_prep_phrase(text):
      if str(oeQA) in str(dpp):
        dpp_earthQA.append(dpp)
    if dpp_earthQA!=[]:
        gpp = max(dpp_earthQA, key = len)
    else:
        gpp = oeQA
    dpp_out_earthQA.append(gpp)
    output_to_SbT= output_to_SbT.replace(gpp,'')
        
  out_to_earthQA = ','.join(dpp_out_earthQA)
  output_to_SbT= output_to_SbT.translate(str.maketrans('','',string.punctuation))
  # output_to_SbT = text.translate(str.maketrans('','',string.punctuation))
  return [output_to_SbT, out_to_earthQA]

def response_enhancement(engine, answer):
    # ... waiting for engines output formats to be decided
    assist_list = ['What else can I help you with?', 'I will be glad to help you with your next request. :)',
                   'What else can I assist you with?', 'Pose another request, please.']
    response = engine + ' answer.\n' + random.choice(assist_list)
    return response


def digital_assistant_to_engine(users_input):
    output_to_engine = {'engine': '',
                        'request':
                            {'text': '',
                             'image': ''}
                        }
    output_to_engines = {'engine': '',
                         'request':
                             {'text': [],
                              'image': ''}
                         }

    # Engine Selection step 1
    # path 'text with image'
    if user_input_format(users_input) == 'text + image':
        # Engine Selection 2a
        output_to_engine['engine'] = engine_selection_2a(users_input['text'])
        output_to_engine['request'] = users_input

    # path 'textual'
    elif user_input_format(users_input) == 'text':
        # in case of complex request
        if SbT_activation(users_input['text']):
            if earthQA_activation(users_input['text']):
                # asking for clarifications
                if request_disambiguation(users_input['text'])['need'] == True:
                    return request_disambiguation(users_input['text'])['message']
                output_to_engines['engine'] = 'SbT & EarthQA'
                output_to_engines['request']['image'] = users_input['image']
                output_to_engines['request']['text'] = complex_request_decompose(users_input['text'])
                return output_to_engines
            else:  # SbT
                output_to_engine['engine'] = 'SbT'
                output_to_engine['request'] = users_input
        elif earthQA_activation(users_input['text']):  # EarthQA
            if request_disambiguation(users_input['text'])['need'] == True:
                return request_disambiguation(users_input['text'])['message']
            output_to_engine['engine'] = 'EarthQA'
            output_to_engine['request'] = users_input
        else:  # no engine to activate => conversational component takes charge
            output_to_engine['engine'] = 'conversational'
            output_to_engine['request'] = users_input
            
        if conversational_activation(users_input['text']):
            output_to_engine['engine'] = 'conversational'
            output_to_engine['request'] = users_input    

    return output_to_engine