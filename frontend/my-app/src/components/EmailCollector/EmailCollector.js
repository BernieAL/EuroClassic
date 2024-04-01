import React,{useState} from 'react'
import module_css from './EmailCollector.module.css'

export default function EmailCollector(){

    const [formSubmitted,setFormSubmitted] = useState(false)

    const handleFormSubmit = async (e) =>{
        e.preventDefault()
        console.log(" email form submitted")
        setFormSubmitted(true)

        // pass collected email back up to parent to be passed to api through another request or just create request to api and send from here
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