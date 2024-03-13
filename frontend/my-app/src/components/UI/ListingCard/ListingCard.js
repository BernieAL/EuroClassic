import React,{useState} from "react"
// import "../../../styles.scss"
// import module_css from './Navbar.module.css'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import mclarenp1 from '../../../images/mclarenp1.jpg';



export default function ListingCard(){

   

    return (
      
        <div className="listing_card">
                    <div className="listing_card_content">
                        <div className="listing_card_img_container">
                            <img className="listing_card_img" src={mclarenp1} alt="" />
                        </div>
                        <div className="listing_card_icon_stats">
                            <div className="listings_change_indicator" 
                                 aria-label="indicator, green or red, showing change num of listings over current 30 days compared to last 30 days">
                                <div className="listing_bottom_icons"> 
                                    <h2 className="icon"><FontAwesomeIcon icon={["fas", "arrow-up"]} /></h2>
                                    <h2 className="literal_value_change">120</h2>
                                </div>
                            </div>
                            <div className="listings_change_indicator" 
                                 aria-label="indicator, green or red, showing change num of listings over current 30 days compared to last 30 days">
                                <div className="listing_bottom_icons"> 
                                    <h2 className="icon"><FontAwesomeIcon icon={["fas", "arrow-up"]} /></h2>
                                    <h2 className="literal_value_change">120</h2>
                                </div>
                            </div>
                            <div className="listings_change_indicator" 
                                 aria-label="indicator, green or red, showing change num of listings over current 30 days compared to last 30 days">
                                <div className="listing_bottom_icons"> 
                                    <h2 className="icon"><FontAwesomeIcon icon={["fas", "arrow-up"]} /></h2>
                                    <h2 className="literal_value_change">120</h2>
                                </div>
                            </div>
                            
                            
                           
                            {/* <p className="sold_change_30_days">change is sold transactions over last 30 days compared to last 30 days</p>
                            <p className="price_avg_30_days">numerical dollar value of change is avg listing price compared to last 30 days</p> */}
                        </div>
                        <button className="view_result">View Result Set</button>
                    </div>
                </div>
    )    
    }