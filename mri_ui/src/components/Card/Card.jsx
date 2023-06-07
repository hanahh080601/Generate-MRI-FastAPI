import React from "react";

import "./card.css"
import CardItem from "../Card/CardItem";

export default function Card({ res }) {
    console.log("render")
    return <div className="card-container">
        <div className="card-container-display">
            <CardItem image_url={res["source_path"]} contrast={'source ' + res["source_contrast"]} />
            <CardItem image_url={res["generated_path"]} contrast={'generated ' + res["target_contrast"]} />
            <CardItem image_url={res["ground_truth_path"]} contrast={'real ' + res["target_contrast"]} /> 
        </div>
    </div>
}
