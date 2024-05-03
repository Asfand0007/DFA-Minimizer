from visual_automata.fa.dfa import VisualDFA
import cv2

def invert_colors(image_path, fileName="dfa"):
    image = cv2.imread(image_path)
    inverted_image = 255 - image
    inverted_image_path = f"{fileName}.png"
    cv2.imwrite(inverted_image_path, inverted_image)

    return inverted_image_path

def getDFA(statesList, transitionsList, initialState, finalStates, fileName="dfa"):
    dfa = VisualDFA(
        states=statesList,
        input_symbols={"0", "1"},
        transitions=transitionsList,
        initial_state=initialState,
        final_states=finalStates,
    )

    graph = dfa.show_diagram()
    graph.render(fileName, format='png')
    return invert_colors(f"{fileName}.png", fileName=fileName)


def helperMinimize(stateI, statesSet, visited, states, table):
    statesSet.add(stateI)
    if visited[stateI]:
        return
    
    visited[stateI]=True

    for stateJ in states:
        if stateJ > stateI:
            if not table[stateJ][stateI]:
                table[stateJ][stateI]= True
                if not visited[stateJ]:
                    helperMinimize(stateJ, statesSet, visited, states,table)
        elif stateJ < stateI:
            if not table[stateI][stateJ]:
                table[stateI][stateJ]= True
                if not visited[stateJ]:
                    helperMinimize(stateJ, statesSet, visited, states,table)

def getMinimizedDFA(allStates,transitions,initialState,finalStates):
    table={}
    
    #removing inaccessible states
    stateRemoved= True
    while stateRemoved:
        stateRemoved= False
        accessibleStates=set()
        accessibleStates.add(initialState)
        for state in allStates:
            accessibleStates.add(transitions[state]['0'])
            accessibleStates.add(transitions[state]['1'])
        if len(accessibleStates)<len(allStates):
            stateRemoved=True
            allStates=accessibleStates
    
    states= sorted(allStates)
    for stateI in states:
        table[stateI]= {}       
        for stateJ in states:
            if (stateI in finalStates and stateJ in finalStates) or (stateI not in finalStates and stateJ not in finalStates):
                table[stateI][stateJ]=False
            else:
                table[stateI][stateJ]=True

    flag= True
    while flag:
        flag=False
        for stateI in table:
            for stateJ in table[stateI]:
                if stateI==stateJ:
                    break
                if table[stateI][stateJ]==False:
                    a0=transitions[stateI]['0']
                    b0=transitions[stateJ]['0']
                    if table[a0][b0]:
                        flag=True
                        table[stateI][stateJ]=True
                        continue
                    a1=transitions[stateI]['1']
                    b1=transitions[stateJ]['1']
                    if table[a1][b1]:
                        flag=True
                        table[stateI][stateJ]=True
                        continue
            
    # # printing table
    # for key in table:
    #     for key2 in table[key]:
    #         print(int(table[key][key2]), end=" ")
    #     print()

    visited= {state: False for state in states}
    newStates={}
    
    for state in states:
        if not visited[state]:
            statesSet= set()
            helperMinimize(state,statesSet,visited, states, table)
            newStates[f"s{len(newStates)}"]=statesSet

    print("New states:")
    for key in newStates:
        print(key,":",newStates[key])

    newFinalStates=set()
    newTransitions={}
    newInitialState= ""
    
    for key in newStates:
        if initialState in newStates[key]:
            newInitialState=key
            break

    for state in newStates:
        oldState=next(iter(newStates[state]))
        if oldState in finalStates:
            newFinalStates.add(state)

        t0= transitions[oldState]["0"]
        t1= transitions[oldState]["1"]
        newTransitions[state]={}
        for stateJ in newStates:
            if t0 in newStates[stateJ]:
                newTransitions[state]['0']= stateJ
            if t1 in newStates[stateJ]:
                newTransitions[state]['1']= stateJ

    print("New transitions:")
    for transition in newTransitions:
        print(transition,":", newTransitions[transition])
    
    print("Initial state:",newInitialState)
    print("Final states:",newFinalStates)

    return getDFA(set(newStates.keys()),newTransitions,newInitialState,newFinalStates, fileName="minimisedDFA")