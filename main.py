#unDumped = [{'TIMESTEP':int, 'NUMBER OF ATOMS':int, 'BOX BOUNDS':dict specific to each boundary condition}, 'ATOMS':[dict specific to dump style]}]
#pp dict: {'x':[x1,x2], 'y':[y1,y2].'z':[z1,z2]}
#id type scaled positions {'id':str, 'type':str, 'xs':str, 'ys':str, 'zs':str}
#id type element positions {'id':str, 'type':str, 'element':str, 'x':str, 'y':str, 'z':str}


def read_whole_dump(file:str) -> list[dict[str:any]]:
    """read the entire file into an unDumped data structure"""
    lineCount = 0 #keeps track of what line we are in a given frame
    frameCount = -1 #keeps track of what frame we are in, starts at =1 because the first frame is considered the 0th frame
    unDumped = [] #intializing the final return object
    
    with open(file) as myfile:
        for line in myfile:
            lineCount += 1
            if "TIMESTEP" in line: #how we know we are in a new frame
                lineCount = 1 #resets the lineCount every frame
                frameCount += 1 #updates the frameCount when we enter a new frame
                unDumped.append({"TIMESTEP":0 , "NUMBER OF ATOMS":0 , "BOX BOUNDS":{} , "ATOMS": [] }) #skeleton of the final output data structure
            if lineCount == 2: #The line in a frame that contains the time step information
                unDumped[frameCount]["TIMESTEP"] = int(line) #updates the value of the TIMESTEP key
            elif lineCount == 4:
                unDumped[frameCount]["NUMBER OF ATOMS"] = int(line) #updates the value of the NUMBER OF ATOMS key
            elif lineCount == 5: #the line that contains information about the boundary conditions
                if "pp" in line: #logic that determines the format of the value of BOX BOUNDS
                    unDumped[frameCount]["BOX BOUNDS"] = {"x":[], "y":[], "z":[]}
            elif lineCount == 6: # lines that contain values of BOX BOUNDS, will be organized depending on boundary type
                unDumped[frameCount]["BOX BOUNDS"]["x"] = line.split()
            elif lineCount == 7:
                unDumped[frameCount]["BOX BOUNDS"]["y"] = line.split()
            elif lineCount == 8:
                unDumped[frameCount]["BOX BOUNDS"]["z"] = line.split()
            elif lineCount == 9: #line that contains information about the atom information being dumped, generates format of output dictionary 
                v_line = line.split() #store all the parameters in a list
            elif lineCount >= 10: #lines 10 and up contain dump data of each atom
                s_line = line.split() #store all the values in a list
                paraCount = 0 #intializing a parameter count that keeps track of how many parameters specifty an atom
                atomDict = {} #creating an empty dict for every new atom
                for para in v_line: #iterating over each parameter to store it for each atom
                    if para != 'ATOMS' and para != 'ITEM:': #ignoring those indicators
                        atomDict[para] = s_line[paraCount] #creating the dictionary pair by pair
                        paraCount += 1 #updating the paraCount to be able to index the list properly
                unDumped[frameCount]["ATOMS"].append(atomDict) #adding the dict specifiying each atom to the final data structure
                
                
    return unDumped


print(read_whole_dump("fcc_Cu_0.lammpstrj"))

                
                