import random
import csv
from collections import defaultdict

import helper_functions as hf


from queries.tv_queries import TVQueries
from queries.tv_templates import TVResponses

class TVFunctions(object):

    # def get_user_award_data():
    #     TVResponses.AWARD_USER_FIRST_RESPONSE

        #show , won_n, det, award,


    # show, genre1, genre2,
    def get_genre_tv_data():
        results = hf.query_sparql(TVQueries.GENRE_INFO)
        all_data = []
        
        restruct_data = {"show":[], "genres":[]}

        for data in results["results"]["bindings"]:
            show = data["tv"]["value"]
            genre1 = data["genre"]["value"]

            response_inits = []
            response_questions = []

            if genre1.split(" ")[-1] == "television":
                genre1 = genre1 + " show"
            s = "" if genre1[-1] == "s" else "s" #what is s? 
            #s is a string that is either empty or "s" depending on whether the last letter of genre1 is "s" or not
            if "genre1" in data or genre2 != genre1:
                genre2 = data["genre1"]["value"]
                if genre2.split(" ")[-1] == "television":
                    genre2 = genre2 + " show"
                s2 = "" if genre2[-1] == "s" else "s"
                triples = [(show, "genre", genre1), (show, "genre", genre2)] #why is this a list of tuples?
                
                response_init_templates = TVResponses.GENRE_SYSTEM_FIRST_RESPONSE["init_2"]
                response_ques_templates = TVResponses.GENRE_SYSTEM_FIRST_RESPONSE["question_2"]
                ques_temp = []
                init_temp = []
                for response_template_str in response_init_templates:
                    response_inits.append(response_template_str.format(show=show,genre1=genre1,genre2=genre2))
                    init_temp.append(response_template_str)
                for response_template_str in response_ques_templates:
                    response_questions.append(response_template_str.format(genre1=genre1,genre2=genre2,s1=s,s2=s2))
                    ques_temp.append(response_template_str)
                all_responses = []
                templates = []
                for i, inits in enumerate(response_inits):
                    for j, quest in enumerate(response_questions):
                        all_responses.append(inits + quest)
                        templates.append(init_temp[i] + ques_temp[j])
                restruct_data["show"].append(show)
                restruct_data["genres"].append(genre1)
                restruct_data["genres"].append(genre2)
            else:
                ques_temp = []
                init_temp = []
                response_init_templates = TVResponses.GENRE_SYSTEM_FIRST_RESPONSE["init_1"]
                response_ques_templates = TVResponses.GENRE_SYSTEM_FIRST_RESPONSE["question_1"]
                triples = [(show, "genre", genre1)]
                for response_template_str in response_init_templates:
                    response_inits.append(response_template_str.format(show=show,genre=genre1,))
                    init_temp.append(response_template_str)
                for response_template_str in response_ques_templates:
                    response_questions.append(response_template_str.format(genre=genre1,s=s))

                    ques_temp.append(response_template_str)
                all_responses = []
                templates = []
                for inits in response_inits:
                    for quest in response_questions:
                        all_responses.append(inits + quest)
                        templates.append(init_temp[i] + ques_temp[j])
                restruct_data["show"].append(show)
                restruct_data["genres"].append(genre1)

            #all_data.append([triples, all_responses, templates, "genre", "tv"])
            all_data.append([triples, all_responses, templates])
        #print(all_data[3])

        random.shuffle(all_data)
        return all_data
        #train = all_data[hf.test_num:]
        #test = all_data[:hf.test_num]
    """def get_award_tv_data():
        #Award
        results = hf.query_sparql(TVQueries.AWARD_INFO)
        # templates_year = TVResponses.AWARD_SYSTEM_FIRST_RESPONSE["intro_year"]
        # templates_noyear = TVResponses.AWARD_SYSTEM_FIRST_RESPONSE["intro_noyear"]
        #
        # templates_question = TVResponses.AWARD_SYSTEM_FIRST_RESPONSE["question"]
        all_data = []
        # show, det, award, year, # number of awards

        for data in results["results"]["bindings"]:
            tv = data['tv']["value"]
            awardlabel = data['award']["value"]
            if "date" in data:
                dateLabel = data['date']["value"].split("-")[0]
                triple = [(tv, "award received", awardlabel), (tv, "date", dateLabel)]
                det = "an" if awardlabel[0].lower() in ['a', 'e', 'i', 'o', 'u'] else "a"
                responses = []
                templates = []
            else:
                triple = [(tv, "award received", awardlabel)]
                det = "an" if awardlabel[0].lower() in ['a', 'e', 'i', 'o', 'u'] else "a"
                templates = []
                responses = []
            all_data.append([triple, responses, templates, "award", "tv"])

        #hf.print_examples(train, test)
        #print("all_data", len(all_data))
        return all_data"""

    def get_tv_award_data():

        results = hf.query_sparql(TVQueries.AWARD_INFO)
        # templates_year = TVResponses.AWARD_SYSTEM_FIRST_RESPONSE["intro_year"]
        # templates_noyear = TVResponses.AWARD_SYSTEM_FIRST_RESPONSE["intro_noyear"]
        #
        # templates_question = TVResponses.AWARD_SYSTEM_FIRST_RESPONSE["question"]
        all_data = []
         #show, det, award, year, # number of awards

        for data in results["results"]["bindings"]:
            tv = data['tv']["value"]
            awardlabel = data['award']["value"]
            if "date" in data:
                dateLabel = data['date']["value"].split("-")[0]
                triple = [(tv, "award received", awardlabel), (tv, "date", dateLabel)]
                det = "an" if awardlabel[0].lower() in ['a', 'e', 'i', 'o', 'u'] else "a"
                responses = []
                templates = []
                # if dateLabel:
                #     for template in templates_year:
                #         for tp in templates_question:
                #             responses.append(template.format(
                #                 show=tv,
                #                 award=awardlabel,
                #                 det = det,
                #                 year=dateLabel).strip()+tp)
                #             templates.append(template)
            else:
                triple = [(tv, "award received", awardlabel)]
                det = "an" if awardlabel[0].lower() in ['a', 'e', 'i', 'o', 'u'] else "a"
                templates = []
                responses = []
                # for template in templates_noyear:
                #     for tp in templates_question:
                #         responses.append(template.format(
                #             show=tv,
                #             award=awardlabel,
                #             det = det).strip()+tp)
                #         templates.append(template)
            all_data.append([triple, responses, templates, "award", "tv"])

        random.shuffle(all_data)
        train = all_data[hf.test_num:]
        test = all_data[:hf.test_num]

        # hf.print_examples(train, test)

        return train, test


    def get_tv_creator_show_data():

        results = hf.query_sparql(TVQueries.CREATOR_SHOWS)
        templates_other_shows_directed = TVResponses.CREATOR_USER_FIRST_RESPONSE["other_shows_creator"]
      #  templates_other_shows_directed = TVResponses.CREATOR_SYSTEM_FIRST_RESPONSE["intro_other_shows_directed"]
        question = TVResponses.CREATOR_SYSTEM_FIRST_RESPONSE["question"]
        #templates_other_shows_creator = TVResponses.AWARD_SYSTEM_FIRST_RESPONSE["intro_noyear"]


        all_data = []
         #show, det, award, year, # number of awards

        for data in results["results"]["bindings"]:
            label = "creator_show"
            show1 = data["tv"]['value']
            creator = data["creator"]['value']
            gender = data["gender"]['value'] if "gender" in data else ""
            creator_id = data["creatorNode"]['value']
            show2 = data["show"]['value']
            start = data["start"]['value'] if "start" in data else ""
          #  end = data["end"]
           # self.named_entities[creator] = {"entity_type_dbpedia": "Person", "wiki_id": creator_id, "gender": gender}
            triple = [(show1, "creator", creator)]
            # if response_num == 1:
            response_templates = []
            templates = []
            for response_template_str in templates_other_shows_directed:
                response_templates.append(response_template_str.format(
                    show=show1,
                    creator=creator,
                    poss=hf.getPronouns(gender, val_type="poss")
                ))
                templates.append(response_template_str)

            all_data.append([triple, response_templates,  templates,  "show_creator",  "tv"])

        random.shuffle(all_data)
        train = all_data[hf.test_num:]
        test = all_data[:hf.test_num]

        # hf.print_examples(train, test)

        return train, test

    def creator_show_data_2():
        results = hf.query_sparql(TVQueries.CREATOR_SHOWS)
        all_data = []
        for data in results["results"]["bindings"]:
            label = "creator_show"
            show1 = data["tv"]['value']
            creator = data["creator"]['value']
            gender = data["gender"]['value'] if "gender" in data else ""
            creator_id = data["creatorNode"]['value']
            show = data["show"]['value']
            start = data["start"]['value'].split("-")[0] if "start" in data else ""
            end = data["end"]['value'].split("-")[0] if "end" in data else ""
            response_init = []
            response_question = []
            templates = []
            if label == "creator_show":
                response_question = TVResponses.CREATOR_USER_SECOND_RESPONSE["question_show"]
                if start == "":
                    for response_template_str in TVResponses.CREATOR_USER_SECOND_RESPONSE["creator"]["no_year"]:
                        for i in response_question:
                            response_init.append(response_template_str.format(
                                show=show,
                                creator=creator
                            )+i)
                            templates.append(response_template_str)
                    triple = [(show, "creator", creator)]
                else:
                    for response_template_str in TVResponses.CREATOR_USER_SECOND_RESPONSE["creator"]["year"]:
                        for i in response_question:
                            response_init.append(response_template_str.format(
                                show=show,
                                creator=creator,
                                start=start
                            ) + i)
                            templates.append(response_template_str)
                    triple = [(show, "creator", creator), (show, "start time", start)]



            all_data.append([triple, response_init, templates, "show_creator", "tv"])

        random.shuffle(all_data)
        train = all_data[hf.test_num:]
        test = all_data[:hf.test_num]

        # hf.print_examples(train, test)

        return train, test





        # # show, genre1, genre2,
        # def genre_data():
        #     results = hf.query_sparql(TVQueries.GENRE_INFO)
        #
        #     for data in results["results"]["bindings"]:
        #         show = data["show"]["value"]
        #         genre1 = data["genre"]["value"]
        #
        #         response_inits = []
        #         response_questions = []
        #
        #         if genre1.split(" ")[-1] == "television":
        #             genre1 = genre1 + " show"
        #         genre1_id = data["genre"]["genre1_id"]
        #         s = "" if genre1[-1] == "s" else "s"
        #
        #         if "genre2" in data:
        #             genre2 = data["genre1"]["value"]
        #             if genre2.split(" ")[-1] == "television":
        #                 genre2 = genre2 + " show"
        #
        #             s2 = "" if genre2[-1] == "s" else "s"
        #
        #             if self.curr_init_user:
        #                 response_init_templates = TVResponses.GENRE_USER_FIRST_RESPONSE["init_2"]
        #                 response_ques_templates = TVResponses.GENRE_USER_FIRST_RESPONSE["question_2"]
        #             else:
        #                 response_init_templates = Responses.GENRE_SYSTEM_FIRST_RESPONSE["init_2"]
        #                 response_ques_templates = Responses.GENRE_SYSTEM_FIRST_RESPONSE["question_2"]
        #
        #             for response_template_str in response_init_templates:
        #                 response_inits.append(response_template_str.format(
        #                     show=self.curr_entity,
        #                     genre1=genre1,
        #                     genre2=genre2
        #                 ))
        #             for response_template_str in response_ques_templates:
        #                 response_questions.append(response_template_str.format(
        #                     genre1=genre1,
        #                     genre2=genre2,
        #                     s1=s,
        #                     s2=s2
        #                 ))
        #         else:
        #             if self.curr_init_user:
        #                 response_init_templates = TVResponses.GENRE_USER_FIRST_RESPONSE["init_1"]
        #                 response_ques_templates = TVResponses.GENRE_USER_FIRST_RESPONSE["question_1"]
        #             else:
        #                 response_init_templates = TVResponses.GENRE_SYSTEM_FIRST_RESPONSE["init_1"]
        #                 response_ques_templates = TVResponses.GENRE_SYSTEM_FIRST_RESPONSE["question_1"]
        #
        #             for response_template_str in response_init_templates:
        #                 response_inits.append(response_template_str.format(
        #                     show=self.curr_entity,
        #                     genre=genre1,
        #                 ))
        #             for response_template_str in response_ques_templates:
        #                 response_questions.append(response_template_str.format(
        #                     genre=genre1,
        #                     s=s
        #                 ))
        #
        #         response_alternatives = [response_inits, response_questions]

    def get_character_info():
        results = hf.query_sparql(TVQueries.CHARACTER_INFO)
        templates = TVResponses.CHARACTER_SYSTEM_FIRST_RESPONSE
        templates_char_user_sec = TVResponses.CHARACTER_USER_SECOND_RESPONSE

        templates_user_first_response = TVResponses.AWARD_USER_FIRST_RESPONSE
        all_data = []
        # show, det, award, year, # number of awards
        for data in results["results"]["bindings"]:
            musician = data['musicianLabel']["value"]
            awardlabel = data['awardLabel']["value"]
            dateLabel = data['date']["value"]
            triple = (musician, "label", awardlabel)
            templates = []
            responses = []
            for template in templates:
                responses.append(template.format(
                    reclab=awardlabel,
                    new_mus=musician).strip())
            all_data.append([triple, responses])

        random.shuffle(all_data)
        train = all_data[hf.test_num:]
        test = all_data[:hf.test_num]

        # hf.print_examples(train, test)

        return train, test

