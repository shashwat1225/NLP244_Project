"""
Start with (only query without a filter by an entity
--> Genre Info

Join
  --> Award Info by TV name, extract info from genre first then award info
  --> Creator Shows by TV name, extract info from genre info then run creator shows
  --> CREATOR_DIRECTED_OTHER by TV name/show, extract info from genre info then run created directed other
  --> ACTOR_SWITCH_INFOR by TV name/show, extract info from genre info then run function
  -->
"""

class TVQueries(object):
    GENRE_INFO = """
        SELECT ?tv ?genre ?genre1 ?genreNode
                WHERE 
                {
                ?TVType wdt:P31 wd:Q5398426.
                ?TVType rdfs:label ?tv.
                FILTER (LANG(?tv) = "en").               

                ?TVType wdt:P136 ?genreNode.
                ?genreNode rdfs:label ?genre.
                  FILTER(LANG(?genre) = "en") . 

                  ?TVType wdt:P136 ?genreNode1.
                ?genreNode1 rdfs:label ?genre1.
                  FILTER(LANG(?genre1) = "en") . 
                } LIMIT 5
        """
    AWARD_INFO = """
       SELECT  ?tv ?award ?date
        WHERE 
        {


          ?TVType wdt:P31 wd:Q5398426.
          ?TVType rdfs:label ?tv.
          FILTER (LANG(?tv) = "en").
          FILTER (STR(?tv) = "Breaking Bad").


          ?TVType p:P166 ?awardInfo.
          ?awardInfo ps:P166 ?awardNode.

          {?awardNode wdt:P31 ?idType.}
          UNION
          {?awardNode wdt:P31 ?idNode .
           ?idNode wdt:P279 ?idType.}
          UNION
          {?awardNode wdt:P31 ?idNode1 .
           ?idNode1 wdt:P279 ?idNode2.
           ?idNode2 wdt:P279 ?idType.}

          ?awardNode rdfs:label ?award .
          FILTER(LANG(?award) = "en") .
          OPTIONAL{
            ?awardInfo pq:P585 ?date .
          }
            }

    """

    CREATOR_SHOWS = """
                    SELECT ?tv ?creator ?creatorNode ?gender ?show ?showNode ?start ?end
                   WHERE
                   {
                     ?TVType wdt:P31 wd:Q5398426.
                     ?TVType rdfs:label ?tv.
                     FILTER (LANG(?tv) = "en").
                     FILTER (STR(?tv) = "Breaking Bad").
                      
                     ?TVType wdt:P170 ?creatorNode.
                     ?creatorNode rdfs:label ?creator .
                     FILTER(LANG(?creator) = "en") .

                     OPTIONAL{
                       ?creatorNode wdt:P21 ?genderNode.
                       ?genderNode rdfs:label ?gender .
                     FILTER(LANG(?gender) = "en") .}

                      {?showNode wdt:P170 ?creatorNode.}
                       UNION
                     {
                       ?showNode wdt:P1431 ?creatorNode.}

                     ?showNode rdfs:label ?show .
                     ?showNode wdt:P31/wdt:P279* wd:Q5398426.
                      FILTER(LANG(?show) = "en") .

                     OPTIONAL{
                       ?showNode wdt:P580 ?start.
                       ?showNode wdt:P582 ?end.
                       } 
                   } """

    CREATOR_DIRECTED_OTHER = """
                   %s

                   SELECT ?creator ?creatorNode ?gender ?show ?showNode ?episode (SAMPLE(?date) as ?date)
                   WHERE
                   {
                     BIND(wd:%s AS ?item).

                     ?item wdt:P170 ?creatorNode.
                     ?creatorNode rdfs:label ?creator .
                     FILTER(LANG(?creator) = "en") .
                     FILTER (STR(?creator) = "Vince Gilligan").
                     
                     OPTIONAL{
                       ?creatorNode wdt:P21 ?genderNode.
                       ?genderNode rdfs:label ?gender .
                     FILTER(LANG(?gender) = "en") .}

                       ?episodeNode wdt:P57 ?creatorNode.
                     ?episodeNode wdt:P179 ?showNode.
                     FILTER(?showNode != ?item).
                     ?episodeNode rdfs:label ?episode .
                     ?episodeNode wdt:P31/wdt:P279* wd:Q21191270.
                      FILTER(LANG(?episode) = "en") .
                     ?showNode rdfs:label ?show .
                     #?showNode wdt:P31/wdt:P279* wd:Q5398426.
                      FILTER(LANG(?show) = "en") .

                      OPTIONAL{
                       ?episodeNode wdt:P577 ?date.
                       }
                   } GROUP BY ?creator ?creatorNode ?gender ?show ?showNode ?episode """

    creator_directed_same = """
                   %s

                   SELECT ?creator ?creatorNode ?gender ?episode ?episodeNode (SAMPLE(?date) as ?date)
                   WHERE
                   {
                     BIND(wd:%s AS ?item).

                     ?item wdt:P170 ?creatorNode.
                     ?creatorNode rdfs:label ?creator .
                     FILTER(LANG(?creator) = "en") .
                     FILTER (STR(?creator) = "Vince Gilligan").

                     OPTIONAL{
                       ?creatorNode wdt:P21 ?genderNode.
                       ?genderNode rdfs:label ?gender .
                     FILTER(LANG(?gender) = "en") .}

                       ?episodeNode wdt:P57 ?creatorNode.
                     ?episodeNode wdt:P179 ?item.
                     ?episodeNode rdfs:label ?episode .
                     ?episodeNode wdt:P31/wdt:P279* wd:Q21191270.
                      FILTER(LANG(?episode) = "en") .

                     OPTIONAL{
                       ?episodeNode wdt:P577 ?date.
                       }
                   } GROUP BY ?creator ?creatorNode ?gender ?episode ?episodeNode """

    ACTOR_SWITCH_INFOR = """
                   %s

                   SELECT ?cast ?castNode ?gender ?show ?showNode ?numEps (COUNT(?oedge) as ?count)
                   WHERE
                   {
                   BIND(wd:%s AS ?item).

                     ?item p:%s ?castInfo.
                         ?castInfo ps:%s ?castNode.
                         ?castNode rdfs:label ?cast .
                         FILTER(LANG(?cast) = "en") .
                         

                         ?castInfo pq:P453 ?roleNode .

                     OPTIONAL{
                       ?castNode wdt:P21 ?genderNode.
                       ?genderNode rdfs:label ?gender .
                     FILTER(LANG(?gender) = "en") .}

                      ?showNode wdt:%s ?castNode.
                      {?showNode wdt:P31 wd:Q5398426.}
                      UNION
                      {?showNode wdt:P31 wd:Q581714.}

                      ?showNode rdfs:label ?show .
                      %s
                      FILTER(LANG(?show) = "en") .
                      FILTER (STR(?show) = "{entity}").

                     {?otheri ?oedge ?castNode .
                     FILTER ( ?oedge in (wdt:P161, wdt:P725) )}
                       UNION
                     {?castNode ?oedge ?otherj .
                     FILTER ( ?oedge in (wdt:P166) )}

                     ?showNode wdt:P1113 ?numEps.

                 } GROUP BY ?cast ?castNode ?gender ?show ?showNode ?numEps ORDER BY DESC(?count)
                 DESC(?numEps)"""

    get_actor_switch_info_complete = """
                   %s

                   SELECT ?cast ?castNode ?gender ?show ?showNode ?imdb ?numEps (COUNT(?oedge) as ?count)
                   WHERE
                   {
                   BIND(wd:%s AS ?item).

                   ?item wdt:%s ?castNode.
                     ?castNode rdfs:label ?cast .
                     FILTER(LANG(?cast) = "en") .
                     
                     
                     OPTIONAL{
                       ?castNode wdt:P21 ?genderNode.
                       ?genderNode rdfs:label ?gender .
                     FILTER(LANG(?gender) = "en") .}

                      ?showNode wdt:%s ?castNode.
                      {?showNode wdt:P31 wd:Q5398426.}
                      UNION
                      {?showNode wdt:P31 wd:Q581714.}

                      ?showNode rdfs:label ?show .
                      %s
                      FILTER(LANG(?show) = "en") .
                      FILTER (STR(?show) = "{entity}").
                      ?showNode wdt:P345 ?imdb.
                      
                      
                     {?otheri ?oedge ?castNode .
                     FILTER ( ?oedge in (wdt:P161, wdt:P725) )}
                       UNION
                     {?castNode ?oedge ?otherj .
                     FILTER ( ?oedge in (wdt:P166) )}

                     ?showNode wdt:P1113 ?numEps.

                 } GROUP BY ?cast ?castNode ?gender ?show ?showNode ?imdb ?numEps ORDER BY DESC(?count)
                 DESC(?numEps)"""

    CHARACTER_INFO = """


                    SELECT ?cast ?castNode ?role ?roleNode ?gender ?award ?awardNode
                    WHERE
                    {
                      BIND(wd:%s AS ?item).

                      ?item p:%s ?castInfo.
                      ?castInfo ps:%s ?castNode.
                      ?castNode rdfs:label ?cast .
                      FILTER(LANG(?cast) = "en") .
                      FILTER (STR(?cast) = "{entity}").
                      
                      ?castInfo pq:P453 ?roleNode .
                      ?roleNode rdfs:label ?role .
                      FILTER(LANG(?role) = "en") .

                      OPTIONAL{
                        ?castNode wdt:P21 ?genderNode.
                        ?genderNode rdfs:label ?gender .
                        FILTER(LANG(?gender) = "en") .}

                      OPTIONAL{
                        ?item p:P166 ?awardInfo.
                        ?awardInfo pq:P1346 ?castNode.
                        ?awardInfo ps:P166 ?awardNode.
                        ?awardNode rdfs:label ?award .
                        FILTER(LANG(?award) = "en") .
                        }

                    } """

    character_system_info = """


                    SELECT ?cast ?castNode ?role ?roleNode ?gender (COUNT(?oedge) as ?count)
                    WHERE
                    {
                      BIND(wd:%s AS ?item).

                      ?item p:%s ?castInfo.
                      ?castInfo ps:%s ?castNode.
                      ?castNode rdfs:label ?cast .
                      FILTER(LANG(?cast) = "en") .
                      FILTER (STR(?cast) = "{entity}").
                      
                      ?castInfo pq:P453 ?roleNode .
                      ?roleNode rdfs:label ?role .
                      FILTER(LANG(?role) = "en") .

                      OPTIONAL{
                        ?castNode wdt:P21 ?genderNode.
                        ?genderNode rdfs:label ?gender .
                        FILTER(LANG(?gender) = "en") .}

                      {?otheri ?oedge ?castNode .
                      FILTER ( ?oedge in (wdt:P161, wdt:P725) )}
                           UNION
                       {?castNode ?oedge ?otherj .
                       FILTER ( ?oedge in (wdt:P166) )}


                    } GROUP BY ?cast ?castNode ?role ?roleNode ?gender ORDER BY DESC(?count) LIMIT 5
                                """

