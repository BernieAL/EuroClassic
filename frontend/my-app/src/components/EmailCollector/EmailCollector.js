import React,{useState} from 'react'
import module_css from './EmailCollector.module.css'

export default function EmailCollector({ user_uuid_prop, ROOT_API_URL}){

    const [formSubmitted,setFormSubmitted] = useState(false)
    const [user_email, setUserEmail] = useState(null)
    const [user_uuid, setUserUUID] = useState(user_uuid_prop)



    const callServer = async(data)=>{
        console.log("callServer rec'd data: ",data)
        try {
            const specificRoute = "update_email"
            const fullURL = `${ROOT_API_URL}/${specificRoute}`
            const response = await fetch(fullURL,{
                method:'POST',
                headers:{
                    'Content-Type':'application/json',
                },
                body:JSON.stringify(data)
            })

            if (!response.ok){
                throw new Error('Problem with response from server')
            } else {
                const responseData = await response.json()
                console.log('EMAIL FORM submitted successfully, RESPONSE:  ', responseData)
            }
        } catch (error) {
            console.error('Error with form submission', error.message)
        } finally {
            console.log('')
        }
    }

    const handleFormSubmit = async (e) =>{
        e.preventDefault()
        
        let email = e.target.email_input.value
        console.log(email)
        setUserEmail(email)
        
        console.log(" email form submitted")
        setFormSubmitted(true)
        
        const email_with_uuid = {
            'uuid': user_uuid_prop,
            'email': email
        };

        callServer(email_with_uuid)
    }

    return (

        <div>
            <div id={module_css.email_input_wrapper}>              
                {formSubmitted === false &&
                    <form onSubmit={handleFormSubmit}>
                        <h1>Veh not found in db - We'll perform a scrape and analysis, then email you the results when ready</h1>
                        <label>
                            <input 
                                type='text'
                                name='email_input'
                                placeholder='your email here'
                            />       
                        </label>
                        <button type='submit'>Submit</button>
                    </form>
                }
                {formSubmitted === true && 
                    <h2>FORM SUBMITTED SUCCESSFULLY, WE WILL EMAIL YOU WITH A LINK TO THE RESULTS</h2>
                }
            </div>
        </div>

    )
}