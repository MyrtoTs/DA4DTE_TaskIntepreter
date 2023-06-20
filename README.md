# DA4DTE_TaskIntepreter
The Task Interpreter’s main target is for the assistant to act as an integrated whole instead of a number of individual engines. 

![image](https://github.com/MyrtoTs/DA4DTE_TaskIntepreter/assets/42088027/7904b237-cb72-4f07-880a-ac2684f84924)

Task Interpreter (TI) is designed to work in collaboration with the UI that will be implemented by e-Geos (see images 2 and 3, containing the suggestion of the UoA team on that). Following is a description of the request’s flow from the user to the engines via the TI as well as the flow of the response back to the user. 
First of all, the DA greets the user and asks them to pose a request (see image 2). Several suggestions (examples that DA is designed to answer) are also offered to the user.

![image](https://github.com/MyrtoTs/DA4DTE_TaskIntepreter/assets/42088027/6f09d97b-2313-480e-95b2-c36cff975e9c)

The user poses a request to the DA, which is passed to the TI. This request can either be only textual or textual with an image. The input cannot contain an image alone, it should be accompanied with the appropriate instruction. So, based on its format, the request can flow in two different paths:
1.	Path with ‘textual with an image’ input.
With such an input format the DA can perform either of two tasks: 
•	Search by Image: where the DA is asked to find a number of images similar to the input one, either of the same type (via unimodal image-image retrieval) or of a different type (cross-modal image-image retrieval). This request is posed as the textual input by the user.
•	Visual Question-Answering: where the DA is asked a question (textual input) based on the image (image input). Examples of this textual input are: “How many vessels does this image show?” or “Is this a rural or an urban area?”.
So, TI selects one of these two engines, depending on text similarity with requests that can be answered from each engine. To determine similarity, we use pre-trained BERT embeddings and the scikit-learn library.
2.	Path with ‘textual’ input.
With such an input format the user either asks DA to perform one of two tasks based on the engines or gives a sentence in the context of dialog (e.g., to express thankfulness or dissatisfaction) which does not address any of the engines. The candidate destinations of textual inputs are:
•	Search by Text: where the DA is asked to find a number of images described by a sentence (e.g., an area that includes coniferous forest).
•	EarthQA: where the DA is asked for satellite images satisfying certain criteria, based on metadata but also on geographical features of entities from knowledge graphs. (e.g., Sentinel-2 satellite images that show Mount Etna, have been taken in February 2021 and have cloud cover less than 10%).	
•	Conversational component: if the user’s intention via their textual input, is not to ask any of the engines to perform any task, then the reply is up to the chat/conversational component of the DA.
Given the textual input, the ΤΙ decides whether the user intends to call one of the textually activated engines or not, depending on text similarity with sentences lying in the ‘engine’ and ‘chat’ classes. To determine similarity, pre-trained BERT embeddings and scikit-learn library are used. If there is no intention to call an engine, then the conversational component is the result of the decision. If the case is to call one of the two above-mentioned engines, before doing so, if any ambiguity is detected in the user’s request, there might be one extra sentence exchange with the user to make specifications on their request. An example of an ambiguous request is ‘Show me 10 images with vessels near Genova port’ at which TI asks the user to restate their request replacing ‘near’ with a specific distance and expects a new request from the user such as ‘Show me 10 images with vessels within a distance of 100 km from Genova port’, which will follow the whole process until it reaches the appropriate engine. Since we have a clear textual request to the DA, the TI remains to select one of EarthQA or Search by Text engines to answer it. The choice depends on the presence of geographical world objects. If there exists some, then EarthQA is selected, else TI has to call the Search by Text engine. This is implemented via named entity recognition, using the SpaCy library. 
Now that TI has carefully decided which engine to call, it outputs a json file with the following three keys: a) engine to call, b) textual request, c) image. Then, TI waits for that engine to work and take its response in a json file, again. Depending on the engine’s output, TI enhances the response and sends it to the user and to a memory cell. For example, if the request ‘Is this a rural or an urban area?’ was sent to the visual QA engine, and the engine’s output was ‘rural’, then the TI has both to enrich the answer to a complete sentence and also to encourage the user to continue the dialog (see image 3 for an example of how a dialogue between the user and the DA should be). 

 ![image](https://github.com/MyrtoTs/DA4DTE_TaskIntepreter/assets/42088027/bb733473-7b8a-48ea-a242-b567bb92036f)


As for the memory cell’s role, it is to track the whole dialogue between the user and the DA. This is something useful for the test phase of the DA when we can collect these dialogs with users and use them to address failed cases.   
 
