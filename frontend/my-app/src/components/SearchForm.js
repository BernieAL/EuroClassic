import React, {useState,useEffect} from 'react'





// // Function to make fetch reqeusts and return data
// // All json results from API have same format, the target data is under "Results"[....]
// async function make_request(url) {
  
//     const response = await fetch(url)
//     const data = await response.json();
//     // return data
//     const result = data['Results']
//     return result
//   }

// /* Fetches makes from api and stores in array, returns array*/
// async function fetchAllCarMakers(){
//     // this gets all car manufacturers, extracting names only and populating all_makes_names_only
//     const all_makes_url = "https://vpic.nhtsa.dot.gov/api//vehicles/GetMakesForVehicleType/car?format=json"
//     const all_makes_names_only =[];

//     await make_request(all_makes_url)
//         .then(all_makes_raw =>{
//         for(let maker of all_makes_raw){
//             all_makes_names_only.push(maker['MakeName']);
//         }
//         console.log(all_makes_names_only)
//         })
//         .catch(error=>{
//         console.error('Error',error)
//         })
//     // console.log(all_makes_names_only)
//     return all_makes_names_only
// }

export default function SearchForm({onDataSubmit}){


    let year = ''
    let make = ''
    let model = ''
    // if form submitted and awaiting server response - disable 'submit' button
    const [submitting,setSubmitting] = useState(false)

    const [userInput,setUserInput] = useState({
        search_query:'',
    })
    
    const [formData,setFormData] = useState({
        year:'',
        make:'',
        model:'',
    })

    const [vehMakeCacheData,setVehMakeCacheData] = useState([])

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

    const handleFormSubmit = async (e) =>{
        e.preventDefault()
        
        console.log("form submitted")
        console.log(userInput)
        // update stored search_query in state to be all caps
        
        /* parse response data into tokens
        check if any of the tokens match a year
        check if any of the tokens match a make
        check if any of the otkens match a model based on the make provided
        */
        // console.log(userInput.search_query)
       
        
        /* REGEX EXPLAINED /b is word boundary - ensure that pattern matches whole words
           /d{4} matches exactly 4 digits (year)
        */
        const yearRegex = /\b\d{4}\b/;
        // tokenize entered search query
        const tokens = userInput.search_query.split(/\s+/)
        
        //Find and return the token matches the yearRegex pattern
        year = tokens.find((token)=> yearRegex.test(token))
        const year_token_index = tokens.indexOf(year)
        // create new array of remaining tokens with year token removed
        const tokens_without_year = tokens.filter(token => token !== year)
        
        // out of remaining tokens, check which token is the 'make' by checking it appears in vehMakeCacheData
        for(let token of tokens_without_year){
            if(vehMakeCacheData.includes(token)){
                make = token
                setFormData({
                    ...formData,
                    [formData.make]: make
                })
                break;
            }
        }
        
        
        
    
        //of remaining tokens after year discovered, determine which is token is the make
        //check if token exists is cache_data
       

        // // make call to backend api
        // try{
        //     const response = await fetch('http://127.0.0.1:5000/vehicle-query',{
        //         method: 'POST',
        //         headers: {
        //             'Content-Type':'application/json',
        //         },
        //         body:JSON.stringify(formData)
        //     })
           
        //     if (!response.ok){
        //         throw new Error ('Problem with response from server')
        //     } else {
        //         // render other components to display the data
               
        //         /*Parsing JSON involves asynchronous operations, especially if the response body is large or if the content is being streamed. As a result, await is used to ensure that the parsing is complete before proceeding. */
                
        //         const responseData = await response.json()
        //         console.log('Form submitted successfully',responseData)

        //         //send data back to parent component using parent function
        //         onDataSubmit(responseData)
        //     }
            
        // } catch (error) {
        //     //handle fetch errors
        //     console.error('Error with form submission', error.message)
        // } finally {
            
        //     setSubmitting(false);
        // }
    }

    const handleFormChange = (e)=>{
        setUserInput({
            ...userInput,
            [e.target.name]:e.target.value
        })
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
                    value={userInput.search_query.toUpperCase()} //controlled component - uppercase enforced
                    // onChange={handleFormChange} 
                />       
                </label>
              
                <button type='submit'>Submit</button>
            </form>
        </div>
    )
}