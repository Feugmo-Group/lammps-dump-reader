#unDumped = [{'TIMESTEP':int, 'NUMBER OF ATOMS':int, 'BOX BOUNDS':dict specific to each boundary condition}, 'ATOMS':[dict specific to dump style]}]
#pp dict: {'x':[x1,x2], 'y':[y1,y2].'z':[z1,z2]}
#id type scaled positions {'id':str, 'type':str, 'xs':str, 'ys':str, 'zs':str}
#id type element positions {'id':str, 'type':str, 'element':str, 'x':str, 'y':str, 'z':str}


def read_whole_dump(file: str) -> list[dict[str:any]]:
    """read the entire file into an unDumped data structure"""
    frameCount = -1 #keeps track of what frame we are in, starts at =1 because the first frame is considered the 0th frame
    unDumped = [] #intializing the final return object
    loopCount = 0 #intializes the frame loop counter which keeps track of how many times the loops runs within a given frame

    with open(file, "r") as myfile:
        for line in myfile:
            loopCount += 1 #updates the frame loop count
            if "TIMESTEP" in line: #how we know we are in a new frame
                loopCount = 0 #resets the loop count on a new frame
                mode = "timeStep" #sets the parser "mode", allows the parser to know what information to grab from the next line
                checkLoop = loopCount #keeps track of what the loop number was when the parser saw the title, important because now on the next loop the parser can grab the information it needs
                frameCount += 1 #updates the frameCount when we enter a new frame
                unDumped.append({"ATOMS":[]}) #skeleton of the final output data structure
            if mode == 'timeStep' and (loopCount - checkLoop) == 1: # finds the line that comes after the TIMESTEP title
                unDumped[frameCount]["TIMESTEP"] = int(line) #updates the value of the TIMESTEP key
            if "NUMBER OF ATOMS" in line: #checks for the line with number of atoms title
                mode = "atomNum"
                checkLoop = loopCount #stores the current loop number
            if mode == "atomNum" and (loopCount - checkLoop) == 1: # Identifies the line with the Number of atoms information
                unDumped[frameCount]["NUMBER OF ATOMS"] = int(line) #updates the value of the NUMBER OF ATOMS key
            if "BOX BOUNDS" in line: #the line that contains information about the boundary conditions type
                mode = "bounds"
                checkLoop = loopCount
                unDumped[frameCount]["BOX BOUNDS"] = {"x":[], "y":[], "z":[]} #intializes a dict that will store the BOXBOUNDS information
            if mode == "bounds" and (loopCount - checkLoop) == 1: 
                unDumped[frameCount]["BOX BOUNDS"]["x"] = line.split()
            if mode == "bounds" and (loopCount - checkLoop) == 2: # lines that contain values of BOX BOUNDS
                unDumped[frameCount]["BOX BOUNDS"]["y"] = line.split()
            if mode == "bounds" and (loopCount - checkLoop) == 3:
                unDumped[frameCount]["BOX BOUNDS"]["z"] = line.split()
            if "ITEM: ATOMS" in line: #line that contains information about the atom information being dumped, generates format of output dictionary 
                mode = "atom"
                checkLoop = loopCount
                v_line = line.split() #store all the parameters in a list
            if mode == "atom" and (loopCount - checkLoop) >= 1: #lines after the ITEM ATOMS title contain dump data of each atom
                s_line = line.split() #store all the values in a list
                paraCount = 0 #intializing a parameter count that keeps track of how many parameters specifty an atom
                atomDict = {} #creating an empty dict for every new atom
                for para in v_line: #iterating over each parameter to store it for each atom
                    if para != 'ATOMS' and para != 'ITEM:': #ignoring those indicators
                        atomDict[para] = s_line[paraCount] #creating the dictionary pair by pair
                        paraCount += 1 #updating the paraCount to be able to index the list properly
                unDumped[frameCount]["ATOMS"].append(atomDict) #adding the dict specifiying each atom to the final data structure
                
                
    return unDumped




                
                