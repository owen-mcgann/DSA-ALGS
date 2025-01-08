How to run: 
- if you would like to upload your own matrix, create a .txt file with you flow matrix like the format below. With each line representing a node and the capacties to all of the other nodes:
  [[0,16,13,0,0,0], 
  [0,0,0,12,0,0],
  [0,4,0,0,14,0],
  [0,0,9,0,0,20],
  [0,0,0,7,0,4],
  [0,0,0,0,0,0]]
  - For clarification: here node 0 is equal to this line [0,16,13,0,0,0] and has a capacity to 1 of 16 and 2 of 13.
- Once you have downloaded our project navigate to the main.py and run that file
- Running Ford Fulkerson and Edmonds-Karp:   
    - In order to sucesfully run F.F. and E.K. the user will need to directly change these lines of code within GUI_Handelers.py and Layout_helpers.py: is_bipartite=False (paramater)
    - The is_bipartite paramater will need to be changed to = False for find_next_augmented_path, last_augmented_path & in backb, and forwardb to sucesfully transfer to the correct data for that algorithm
    - Enter a valid source and sink value 
    - Press import file and pick the file with the flow matrix that you want 
    - Then decide if you want to see it in Ford Folkerson or Edmonds-Karp and click the button associated with one. 
    - Press the next button to see each step and the back to see the previous step
- Running Bipartite:
- In order to sucesfully Bipartite Matching the user will need to directly change these lines of code within GUI_Handelers.py and Layout_helpers.py: is_bipartite=True (paramater)
    - The is_bipartite paramater will need to be changed to = True for find_next_augmented_path, last_augmented_path & in backb, and forwardb to sucesfully transfer to the correct data for that algorithm
    - Enter a number of workers and jobs then press generate matrix
    - Read the pops up for an explaintion 
    - Use the next and back buttons the same way as above
