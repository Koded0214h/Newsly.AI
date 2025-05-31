import './Profile2.css';

import VerticalNavbar from '../components/VerticalNavbar';

export default function Profile2() {
  return (
    <div className="flex flex-col md:flex-row">
      <VerticalNavbar />
      <div className="row">
        <div className='col1'>
            <div className='avatar mt-4 ml-20'></div>
                        <h3 className='text-blue-800 text-lg flex mb-4 font-bold'>Personal Details</h3>

                <div className='profile-info'>
                         <span className='label'>Fullname:</span>
                         <span className='value'>Fredrick Jones</span>
                </div>
                <div className='profile-info'>
                       <span className='label'>Email:</span>
                       <span className='value'>fredrickjones@gmail.com</span>
               </div>
                <div className='profile-info'>
                      <span className='label'>Country:</span>
                    <span className='value'>United States of America</span>

            </div>
                <div className='profile-info'>
                     <span className='label'>Language Preference:</span>
                     <span className='value'>English</span>
                </div>
        </div>
        <div className='col2'>
                <h3 className='text-blue-800 text-lg flex mt-9 mb-4 font-bold'>Account Activity</h3>
                 <div className='profile-info'>
                         <span className='label'>Last Login:</span>
                         <span className='value'>2 hours ago</span>
                </div>
                <div className='profile-info'>
                       <span className='label'>Date joined</span>
                       <span className='value'>5th June, 2023</span>
               </div>
                <div className='profile-info'>
                      <span className='label'>Account Status:</span>
                    <span className='value'>Active</span>

            </div>
                                  <h3 className='text-blue-800 text-lg flex mt-9 mb-4 font-bold'>Preferences</h3>
<div className='profile-info'>
                         <span className='label'>Interest:</span>
                         <span className='value'>Politics Entertainment</span>
                </div>
                <div className='profile-info'>
                       <span className='label'>Email Digest Frequency</span>
                       <span className='value'>Weekly</span>
               </div>
                <div className='profile-info'>
                      <span className='label'>Darkmode</span>
                    <span className='value'>Disabled</span>
                    <button className='button'>Edit</button></div>
        </div>
      </div>
    </div>
  );
}