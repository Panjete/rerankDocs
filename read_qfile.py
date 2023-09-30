from lxml import etree


## Reads the topics
## Returns mapping TopicNum -> (TopicNum, Query, Question, Narrative)
def qfile(queryfile):
    parser = etree.XMLParser()
    with open(queryfile, 'r') as docUnAppended:
            docs_string = docUnAppended.read()

    tree = etree.fromstring("<INIT>\n"+ docs_string + "</INIT>", parser)
    t_queries = tree.xpath(".//topic/query/text()")
    t_questions = tree.xpath(".//topic/question/text()")
    t_narratives = tree.xpath(".//topic/question/text()")

    t_num = []
    for t_element in tree.findall(".//topic"):
        t_num.append(int(t_element.get("number")))

    # prune content for processing
    translation_table = str.maketrans("", "", "(),?.:" )
    # prunes full sentences
    def prune(istr):
        #istr = istr.lower()
        istr = istr.split()
        outistr = []
        for issstr in istr:
            outistr.append(issstr.translate(translation_table))
        return outistr


    pruned_queries = list(map(prune, t_queries))
    pruned_questions = list(map(prune, t_questions))
    pruned_narratives = list(map(prune, t_narratives))

    mapping = {}
    for i in range(len(t_num)):
         mapping[t_num[i]] = (t_num[i], prune(t_queries[i]), prune(t_questions[i]), prune(t_narratives[i]))

    return mapping

# mapping = qfile("covid19-topics.xml")
# print("first quer = " , mapping[1])
# print("total units = " , len(mapping.keys()))

