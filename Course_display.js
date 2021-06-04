import React from "react";
import monogodb from "mongodb"
import "./Course_display.css"

export default class Course_display extends React.Component {
    render() {
        return (
            <div>
                <h1>图片</h1>
                <meta name="referrer" content="no-referrer" />
                <img className='img' src='http://i1.hdslb.com/bfs/archive/63e6291c5686c0880677d05988360c2d8a2fba6d.jpg' />

            </div>
        )
    }
}