import React, {useState,useEffect} from 'react'
import {useNavigate} from 'react-router-dom';

export default function SearchForm({onDataSubmit}){


    let year = ''
    let make = ''
    let model = ''

    // if form submitted and awaiting server response - disable 'submit' button
    const [submitting,setSubmitting] = useState(false)
    const [userInput,setUserInput] = useState({
        search_query:null,
    })
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


    // // This effect will run whenever formData is updated
    // useEffect(() => {
    //     console.log('formData updated:', formData);
    
    //     // You can perform additional actions here if needed
    //     }, [formData]);


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

                
                onDataSubmit(responseData) //send data back to parent component using parent function
                navigate('/results')
            }
        } catch (error) {
            console.error('Error with form submission', error.message)
        } finally {
                setSubmitting(false);
        }
    }



    const handleFormSubmit = async (e) =>{
        e.preventDefault()
        
        console.log("form submitted")
       
        /* REGEX EXPLAINED /b is word boundary - ensure that pattern matches whole words
           /d{4} matches exactly 4 digits (year)
        */
        const yearRegex = /\b\d{4}\b/;

        // tokenize entered search query
        let temp = e.target.search_query.value.toUpperCase()
        console.log(typeof(temp))
        const tokens = temp.split(/\s+/)
        
        //Find and return the token matches the yearRegex pattern
        year = tokens.find((token)=> yearRegex.test(token))
        console.log(year)
        setFormData((prevFormData)=>({
            ...prevFormData,
            state_year: year
        }))
        const year_token_index = tokens.indexOf(year)

        // create new array of remaining tokens with year token removed
        const tokens_without_year = tokens.filter(token => token !== year)
        
        // out of remaining tokens, check which token is the 'make' by checking it appears in vehMakeCacheData
        for(let token of tokens_without_year){
            if(vehMakeCacheData.includes(token)){
                make = token
                setFormData((prevFormData) => ({
                    ...prevFormData,
                    state_make: make
                }))
                break;
            }
        }

        // with year and make token extracted, we should be left with model token only
        const tokens_without_year_and_make = tokens_without_year.filter(token => token !== make)
        model = tokens_without_year_and_make[0]
        setFormData((prevFormData) =>({
            ...prevFormData,
            state_model:tokens_without_year_and_make[0]
        }))  
        

        /*workaround to avoid having to wait for async state update.
        in this way: 
            there is no null form submission
            the variables are populated seperatley from state
            and state is also updated
        */
    
        const entered_data = {'year':year,'make':make,'model':model}
        // call to server with parsed data
        callServer(entered_data)


    }


    /* 
    
     // check if state is updated properly before making call
            if (formData.year === null || formData.make === null || formData.model === null) {
                console.error('Form data is not complete. Aborting server call.');
                return;
            }

    need some kind of function to wait until all values in state are not null,
    then perform call to the server


    
    */



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