from .WikiAndSemanticProcessing import Candidate_intros, viableCandidate, init_model


def getProcessedData(similar):
    # secs, noOfSections,sectionContents = Candidate_intros( [("Bruce Willis", 0.903), ("Tom Hanks", 0.804)] )
    secs, noOfSections,sectionContents = Candidate_intros( similar )

    sorted_secs = {k: v for k, v in sorted( secs.items(), key=lambda item: item[1] )}
    init_model()
    candidates = list( sorted_secs.keys() )
    excluded = list()
    selected=list()

    for sec in sorted_secs.keys():
        if sec not in excluded:
            excluded.append(sec)
            selected.append(sec)
            candidates.remove(sec)

            chosen = list()
            for can in candidates:
                if viableCandidate( sec, can ):
                    chosen.append( can )
                    selected.append(can)
            excluded.extend( chosen )
            candidates = [x for x in candidates if x not in chosen]

    # print("Selected ordering :",file=f)
    # print(selected,file=f)
    # print("Average sections needed:",file=f)
    # print(noOfSections,file=f)

    candidate_content=list()
    for s in selected:
        candidate_content.append(sectionContents[s])

    return noOfSections,selected,candidate_content