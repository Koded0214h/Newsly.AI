import { useState } from "react";
import InterestDropdown from "../components/InterestDropdown";

export default function SignUp() {
    const countries = [
  "Aruba", "Afghanistan", "Angola", "Anguilla", "Åland Islands", "Albania", "Andorra",
  "United Arab Emirates", "Argentina", "Armenia", "American Samoa", "Antarctica",
  "French Southern Territories", "Antigua and Barbuda", "Australia", "Austria",
  "Azerbaijan", "Burundi", "Belgium", "Benin", "Bonaire, Sint Eustatius and Saba",
  "Burkina Faso", "Bangladesh", "Bulgaria", "Bahrain", "Bahamas", "Bosnia and Herzegovina",
  "Saint Barthélemy", "Belarus", "Belize", "Bermuda", "Bolivia, Plurinational State of",
  "Brazil", "Barbados", "Brunei Darussalam", "Bhutan", "Bouvet Island", "Botswana",
  "Central African Republic", "Canada", "Cocos (Keeling) Islands", "Switzerland", "Chile",
  "China", "Côte d'Ivoire", "Cameroon", "Congo", "Congo, Democratic Republic of the",
  "Cook Islands", "Colombia", "Comoros", "Cape Verde", "Costa Rica", "Cuba", "Curacao",
  "Christmas Island", "Cayman Islands", "Cyprus", "Czech Republic", "Germany", "Djibouti",
  "Dominica", "Denmark", "Dominican Republic", "Algeria", "Ecuador", "Egypt", "Eritrea",
  "Western Sahara", "Spain", "Estonia", "Ethiopia", "Finland", "Fiji", "Falkland Islands",
  "France", "Faroe Islands", "Micronesia, Federated States of", "Gabon", "United Kingdom",
  "Georgia", "Guernsey", "Ghana", "Gibraltar", "Guinea", "Guadeloupe", "Gambia", "Guinea-Bissau",
  "Equatorial Guinea", "Greece", "Grenada", "Greenland", "Guatemala", "French Guiana", "Guam",
  "Guyana", "Hong Kong", "Heard Island and McDonald Islands", "Honduras", "Croatia", "Haiti",
  "Hungary", "Indonesia", "Isle of Man", "India", "British Indian Ocean Territory", "Ireland",
  "Iran", "Iraq", "Iceland", "Israel", "Italy", "Jamaica", "Jersey", "Jordan", "Japan",
  "Kazakhstan", "Kenya", "Kyrgyzstan", "Cambodia", "Kiribati", "Saint Kitts and Nevis", "Korea, Republic of",
  "Kuwait", "Lao People's Democratic Republic", "Lebanon", "Liberia", "Libya", "Saint Lucia",
  "Liechtenstein", "Sri Lanka", "Lesotho", "Lithuania", "Luxembourg", "Latvia", "Macao",
  "Saint Martin (French part)", "Morocco", "Monaco", "Moldova", "Madagascar", "Maldives",
  "Mexico", "Marshall Islands", "North Macedonia", "Mali", "Malta", "Myanmar", "Montenegro",
  "Mongolia", "Northern Mariana Islands", "Mozambique", "Mauritania", "Montserrat", "Martinique",
  "Mauritius", "Malawi", "Malaysia", "Mayotte", "Namibia", "New Caledonia", "Niger", "Norfolk Island",
  "Nigeria", "Nicaragua", "Niue", "Netherlands", "Norway", "Nepal", "Nauru", "New Zealand", "Oman",
  "Pakistan", "Panama", "Pitcairn", "Peru", "Philippines", "Palau", "Papua New Guinea", "Poland",
  "Puerto Rico", "North Korea", "Portugal", "Paraguay", "Palestine, State of", "French Polynesia",
  "Qatar", "Réunion", "Romania", "Russian Federation", "Rwanda", "Saudi Arabia", "Sudan",
  "South Sudan", "Senegal", "Singapore", "South Georgia and the South Sandwich Islands",
  "Saint Helena", "Solomon Islands", "Sierra Leone", "San Marino", "Somalia", "Saint Pierre and Miquelon",
  "Serbia", "Sao Tome and Principe", "Suriname", "Slovakia", "Slovenia", "Sweden", "Swaziland",
  "Seychelles", "Syrian Arab Republic", "Chad", "Togo", "Thailand", "Tajikistan", "Tokelau",
  "Timor-Leste", "Turkmenistan", "Tunisia", "Tonga", "Turkey", "Trinidad and Tobago", "Tuvalu",
  "Taiwan", "Tanzania", "Ukraine", "Uganda", "United States", "Uruguay", "Uzbekistan",
  "Holy See (Vatican City State)", "Saint Vincent and the Grenadines", "Venezuela", "Virgin Islands, British",
  "Virgin Islands, U.S.", "Vietnam", "Vanuatu", "Wallis and Futuna", "Samoa", "Yemen", "South Africa",
  "Zambia", "Zimbabwe"
];
const languages = [
  "English", "French", "Spanish", "Portuguese", "Arabic", "Mandarin Chinese",
  "Hindi", "Bengali", "Russian", "Japanese", "German", "Korean", "Italian",
  "Turkish", "Swahili", "Urdu", "Persian (Farsi)", "Vietnamese", "Thai",
  "Dutch", "Polish", "Greek", "Hebrew", "Indonesian", "Filipino (Tagalog)",
  "Malay", "Zulu", "Xhosa", "Yoruba", "Igbo", "Hausa", "Tamil", "Telugu",
  "Punjabi", "Amharic", "Somali", "Nepali", "Sinhala", "Ukrainian"
];

const [showPassword, setShowPassword] = useState(false);


const emailDigest = [
    "Daily", "Weekly", "Monthly"
]
const [selectedInterests, setSelectedInterests] = useState([]);
  return (
    <div className="min-h-screen flex items-center justify-center ">
      <div className="bg-white p-10 rounded-[25px] shadow-md w-full max-w-[700px] max-h-[1000px]">
        <h2 className="text-3xl font-bold text-center text-gray-800 mb-6">Create an Account</h2>

        <h3 className="text-1xl font-bold text-center text-gray-800 mb-6">“Hi 👋 I’m your News Assistant. I’ll tailor your news based on your interests. Let’s set you up!”</h3>

        <form className="space-y-4">
            
          <div>
            <label className="block mb-1 font-semibold text-blue-900">Full Name</label>
            <input
              type="text"
              className="w-full border border-gray-300 px-3 py-2 rounded-[25px] focus:outline-none focus:ring focus:border-blue-400 hover:bg-slate-200"
              placeholder="Enter your name"
            />
          </div>

          <div>
            <label className="block mb-1 font-semibold text-blue-900 ">Email</label>
            <input
              type="email"
              className="w-full border  border-gray-300 px-3 py-2 rounded-[25px] focus:outline-none focus:ring focus:border-blue-400 hover:bg-slate-200"
              placeholder="Enter your email"
            />
          </div>

          <div className="relative">
      <label className="block mb-1 font-semibold text-blue-900">Password</label>
      <input
        type={showPassword ? "text" : "password"}
        className="w-full px-3 py-2 border rounded-[25px] hover:bg-slate-200 focus:outline-none focus:ring focus:border-blue-400"
        placeholder="Enter password"
      />
      <button
        type="button"
        onClick={() => setShowPassword(!showPassword)}
        className="absolute right-3 top-9 transform -translate-y-1/2 text-gray-600 -[25px] hover:bg-slate-200"
      >
        <i className={`fa ${showPassword ? "fa-eye-slash" : "fa-eye"} mt-7`} aria-hidden="true"></i>
      </button>
    </div>

           <div className="relative">
      <label className="block mb-1 font-semibold text-blue-900 font-sans"> Confirm Password</label>
      <input
        type={showPassword ? "text" : "password"}
        className="w-full px-3 py-2 border rounded-[25px] hover:bg-slate-200 focus:outline-none focus:ring focus:border-blue-400"
        placeholder="Enter password"
      />
      <button
        type="button"
        onClick={() => setShowPassword(!showPassword)}
        className="absolute right-3 top-9 transform -translate-y-1/2 text-gray-600 -[25px] hover:bg-slate-200 focus:outline-none focus:ring focus:border-blue-400"
      >
        <i className={`fa ${showPassword ? "fa-eye-slash" : "fa-eye"} mt-7`} aria-hidden="true"></i>
      </button>
    </div>
 <div>
<label className="block mb-1 font-semibold text-blue-900">Country</label>
<select className="w-full border border-gray-300 px-3 py-2 rounded-[25px] focus:outline-none focus:ring focus:border-blue-400 text-gray-600 hover:bg-slate-200">
  <option value="">Select your country</option>
  {countries.map((country, idx) => (
    <option key={idx} value={country}>
      {country}
    </option>
  ))}
</select>
</div>
<div>
    <label className="block mb-1 font-semibold text-blue-900">Language</label>
    <select className="w-full p-2 border border-gray-300 rounded-[25px] text-gray-600 hover:bg-slate-200 focus:outline-none focus:ring focus:border-blue-400">
        <option value="">Select your language</option>
        {languages.map((lang, idx) => (
            <option key={idx} value={lang}>
                {lang}
            </option>
        ))}
    </select>
</div>

<div>
    <label className="block mb- font-semibold text-blue-900">Email Digest Frequency</label>
<select className="w-full p-2 border border-gray-300 rounded-[25px] text-gray-600 hover:bg-slate-200 focus:outline-none focus:ring focus:border-blue-400">
  <option value="">Select your Frequency</option>
  {emailDigest.map((emailD, idx) => (
    <option key={idx} value={emailD}>
      {emailD}
    </option>
  ))}
</select>
</div>

<div className="p-4">
<InterestDropdown selected={selectedInterests} setSelected={setSelectedInterests} className="rounded-[25px] text-gray-600"/>
</div>


          <button
            type="submit"
            className="w-full bg-blue-900 text-white py-2 rounded hover:bg-blue-500 transition duration-200"
          >
            Sign Up
          </button>
        </form>

        <p className="text-center text-sm text-gray-600 mt-4">
          Already have an account? <a href="/login" className="text-blue-600 hover:underline">Log in</a>
        </p>

         <button className="text-center text-sm text-gray-600 mt-4 ml-[200px]">
          I accept the <a href="terms" className="text-blue-600 hover: "> Terms and Conditions </a>
          <input
          type="checkbox"/>
        </button>
      </div>
      
    </div>
  );
}


