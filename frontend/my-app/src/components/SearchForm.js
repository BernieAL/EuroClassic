import React, {useState,useEffect} from 'react'
import {useNavigate} from 'react-router-dom';

export default function SearchForm({handleDataFromSearchForm}){


    let year = ''
    let make = ''
    let model = ''

    // if form submitted and awaiting server response - disable 'submit' button
    const [submitting,setSubmitting] = useState(false)
    const [userInput,setUserInput] = useState({search_query:null})

    const navigate = useNavigate();

    const [formData,setFormData] = useState({
        state_year:null,
        state_make:null,
        state_model:null,
    })
    const [vehMakeCacheData,setVehMakeCacheData] = useState([])

    // request vehMakeCacheData from server, store in state
    useEffect(()=>{
        const load_manufacturer_cache = async ()=>{
            try {
                const response = await fetch('http://127.0.0.1:5000/retrieve_cache')
                const data = await response.json()
                setVehMakeCacheData(data)
                console.log(data)
            } catch(error){
                console.log("Error Retrieving cache data from server")
            }
        }
        load_manufacturer_cache()
    },[])// Empty dependency array ensures that this effect runs only once when the component mounts



    const callServer = async(entered_data) => {
        try{
            const response = await fetch('http://127.0.0.1:5000/vehicle-query',{
                method:'POST',
                headers:{
                    'Content-Type':'application/json',
                },
                // body:JSON.stringify(formData)
                body:JSON.stringify(entered_data)
            })
            
            if(!response.ok){
                throw new Error('Problem with response from server')
            } else {
                
                /*Parsing JSON involves asynchronous operations, especially if the response body is large or if the content is being streamed. As a result, await is used to ensure that the parsing is complete before proceeding. */
                const responseData = await response.json()
                console.log('Form submitted successfully',responseData)

                
                handleDataFromSearchForm(responseData) //send data back up to parent component using parent callback function
                navigate('/results') //redirect to results path which renders vehResultPage component
            }
        } catch (error) {
            console.error('Error with form submission', error.message)
        } finally {
                setSubmitting(false);
        }
    }



    const handleFormSubmit = async (e) =>{

        /*This function is called when form is submitted 
          -Extracts form data from submitted form and converts to uppercase -> <Str> Ex. 1994 bmw m5 -> 1994 BMW M5
          -Tokenizes submitted value 
          -Attempts to identify year value in form data using regex pattern /\b\d{4}\b/
                -if no year found, default of 0000 is used
                -set year state var
          -
          -
        */

        e.preventDefault()
        console.log("form submitted")
       
        /* REGEX EXPLAINED -> /b is word boundary - ensure that pattern matches whole words
           /d{4} matches exactly 4 digits (year)
        */
        const yearRegex = /\b\d{4}\b/; //regex pattern for identifying 4 digit year value

        // standardize form data to upppercase
        let temp = e.target.search_query.value.toUpperCase()
        // console.log(typeof(temp))

        //Tokenize form data, splitting at whitespace -> 1999 BMW M3 -> 1999,BMW,M3 
        const tokens = temp.split(/\s+/)
        // console.log(`tokens: ${tokens}`)


        //check wchich token is year value using yearRegex pattern. if no match set year as 0000
        year = tokens.find((token)=> yearRegex.test(token)) || '0000'
        // console.log(year)
        // update state with year value
        setFormData((prevFormData)=>({
            ...prevFormData,
            state_year: year
        }))
        
        // const year_token_index = tokens.indexOf(year)

        // create new array of remaining tokens with year token removed using -> ['BMW', 'M3']
        //filter logic -> only return tokens that dont match year
        const tokens_without_year = tokens.filter(token => token !== year)
        // console.log(tokens_without_year)

        //out of remaining tokens, check which token is the 'make' value by checking if it appears in vehMakeCacheData (file of all make names)
        //The first token that appears in the vehMakeCacheData is the make
        for(let token of tokens_without_year){
            if(vehMakeCacheData.includes(token)){
                make = token
                console.log("MAKE IDENTIFIED: ",make)
                setFormData((prevFormData) => ({
                    ...prevFormData,
                    state_make: make
                }))
                break;
            }
        }

        // with year and make token extracted, we should be left with model token only
        //if more than one token remaining, take the first token of remaining list
        const tokens_without_year_and_make = tokens_without_year.filter(token => token !== make)
        console.log(tokens_without_year_and_make)
        model = tokens_without_year_and_make[0]
        setFormData((prevFormData) =>({
            ...prevFormData,
            state_model:tokens_without_year_and_make[0]
        }))  
        

        /*WORKAROUND - to avoid having to wait for async state update.
            in this way: 
                there can never be a null form submission
                the variables are populated seperatley from state
                and then state is also updated
        */
    
        const entered_data = {'year':year,'make':make,'model':model}
        // console.log(typeof(entered_data))
        
        // call api server with encapsulated form data 
        callServer(entered_data)
    }

    return(
        
        <div className='search-form-wrapper'>
            <form onSubmit={handleFormSubmit}>
                <label>Enter Your Search here:
                <input 
                    type='text'
                    name='search_query'
                    placeholder='Search For A vehicle (ex. Toyota Supra or 2003 M5'
                    // value={userInput.search_query} //controlled component
                    // onChange={handleFormChange} 
                />       
                </label>
              
                <button type='submit'>Submit</button>
            </form>
        </div>
    )
}