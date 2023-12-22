import React, {useState,useEffect} from 'react'


export default function SearchForm({onDataSubmit}){


    let year = ''
    let make = ''
    let model = ''

    // if form submitted and awaiting server response - disable 'submit' button
    const [submitting,setSubmitting] = useState(false)

    const [userInput,setUserInput] = useState({
        search_query:null,
    })
    
    const [formData,setFormData] = useState({
        year:null,
        make:null,
        model:null,
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




    // This effect will run whenever formData is updated
    useEffect(() => {
        console.log('formData updated:', formData);
    
        // You can perform additional actions here if needed
        }, [formData]);


    const callServer = async() => {
        try{
            const response = await fetch('http://127.0.0.1:5000/vehicle-query',{
                method:'POST',
                headers:{
                    'Content-Type':'application/json',
                },
                body:JSON.stringify(formData)
            })
            if(!response.ok){
                throw new Error('Problem with response from server')
            } else {
                
                /*Parsing JSON involves asynchronous operations, especially if the response body is large or if the content is being streamed. As a result, await is used to ensure that the parsing is complete before proceeding. */
                const responseData = await response.json()
                console.log('Form submitted successfully',responseData)

                //send data back to parent component using parent function
                onDataSubmit(responseData)
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
        const tokens = userInput.search_query.split(/\s+/)
        
        //Find and return the token matches the yearRegex pattern
        year = tokens.find((token)=> yearRegex.test(token))
        console.log(year)
        setFormData((prevFormData)=>({
            ...prevFormData,
            year: year
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
                    make: make
                }))
                break;
            }
        }

        // with year and make token extracted, we should be left with model token only
        const tokens_without_year_and_make = tokens_without_year.filter(token => token !== make)
        setFormData((prevFormData) =>({
            ...prevFormData,
            model:tokens_without_year_and_make[0]
        }))  
          
        callServer()
    }


    
    const handleFormChange = (e)=>{
        setUserInput((prevUserInput)=>({
            ...prevUserInput,
            [e.target.name]:e.target.value.toUpperCase()
        }))
        console.log(userInput)
    }

    return(
        
        <div className='search-form-wrapper'>
            <form onSubmit={handleFormSubmit}>
                <label>Enter Your Search here:
                <input 
                    type='text'
                    name='search_query'
                    placeholder='Search For A vehicle (ex. Toyota Supra or 2003 M5'
                    value={userInput.search_query} //controlled component
                    onChange={handleFormChange} 
                />       
                </label>
              
                <button type='submit'>Submit</button>
            </form>
        </div>
    )
}