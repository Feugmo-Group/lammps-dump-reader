
# general format of unDumped as of now {(id,type),(x,y,z)}


#function which loads entire dump file into memory
def read_whole_dump(file):
    #intializing variables
    count = 0    
    timeStep = []
    unDumped = {}
    
    with open(file) as myfile:
        for line in myfile:
            count += 1           #keeps track of what line we are on
            if "TIMESTEP" in line: #resets count every timestep
                count = 1
            if count == 2:
                timeStep.append(line) #appends each timeStep to a list, may use this later to create a new dict for each timeStep
            elif count == 4:
                atomCount = line      #stores atom count, does this change every time step? should it also be a list?
            elif count == 6:
                boundary_x = line.split() #boundary conditions coordinate x
            elif count == 7:
                boundary_y = line.split() ##boundary conditions coordinate y
            elif count == 8:
                boundary_z = line.split() #boundary conditions coordinate z
            elif count >= 10:
                s_line = line.split()     #splits lines at the whitespace
                unDumped[(s_line[0],s_line[1])] = (s_line[2],s_line[3],s_line[4])  #creates the dict mentioned

                    


