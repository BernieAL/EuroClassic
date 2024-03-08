import React, {useState,useEffect  } from 'react'



/* 
    This component displays popup telling
    the user the requested veh is not in db
    and prompts the the user to enter their email to get notified when scrape results are available

*/
export default function VehNotFound(){

    const [userEmail,setUserEmail] = useState(null)
    const handleFormSubmit = (e) => {
        e.preventDefault()
        
        setUserEmail(e.target.email_input.value)
        console.log(e.target.email_input.value)
    }

    return (
        
        <div className='email-input-wrapper'>
            <h3> Oops we dont have data for that vehicle yet. We've added it to our queue of vehciles to gather data on. It shouldnt be too long, we'll send you an email when its ready</h3>
            <form onSubmit={handleFormSubmit}>
                <label>Enter your email here
                <input 
                    type='text'
                    name='email_input'
                    placeholder='your-email'
                />       
                </label>
                <button type='submit'>Submit</button>
            </form>
        </div>
        
    )
}