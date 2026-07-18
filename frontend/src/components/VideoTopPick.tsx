import React from 'react'
import { Link } from 'react-router-dom'


export const Card = () => {

    return (
        <Link to="/videos" className="flex flex-col items-center bg-white border border-gray-200 rounded-lg shadow md:flex-row md:max-w-xl hover:bg-gray-100 dark:border-gray-700 dark:bg-gray-800 dark:hover:bg-gray-700">
            <img 
            className="object-cover w-full rounded-t-lg h-96 md:h-auto md:w-48 md:rounded-none md:rounded-s-lg" 
            src="https://avatars.githubusercontent.com/u/95700260?s=400&u=8a038fc4fa00588887195b84026eb610c9213b4f&v=4" 
            alt="" 
            />
            <div className="flex flex-col justify-between p-4 leading-normal">
                <h5 className="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">Noteworthy technology acquisitions 2021</h5>
                <p className="mb-3 font-normal text-gray-700 dark:text-gray-400">Here are the biggest enterprise technology acquisitions of 2021 so far, in reverse chronological order.</p>
            </div>
        </Link>
    )
}


const VideoTopPick:React.FC = () => {
    

    return (
        <>
            <div className=' py-4'>
                <h3 className='text-xl font-medium pb-2'>
                Top pick for you on videos
                </h3>
                <div className=' grid grid-cols-1 gap-6 md:grid-cols-2'>
                    <Card />
                    <Card />
                    <Card />
                </div>
            </div>
        </>
    )
}


export default VideoTopPick;