export default function Login() {
  return (
    <div className="min-h-screen flex items-center justify-center  bg-[url('https://images.stockcake.com/public/8/7/8/87823ccb-736a-42d7-b76f-e4e6541c52b7_large/digital-waves-flow-stockcake.jpg')] bg-cover bg-center ">
      <div className="bg-white p-8 rounded shadow-md w-full max-w-md blur-none">
        <h2 className="text-2xl font-bold mb-6 text-center">Login to Your Account</h2>

        <form className="space-y-4 h-200">
          <div>
            <label className="block mb-1 font-semibold text-blue-900">Email</label>
            <input
              type="email"
              className="w-full border border-gray-300 px-3 py-2 rounded focus:outline-none focus:ring focus:border-blue-500"
              placeholder="Enter your email"
            />
          </div>

          <div>
            <label className="block mb-2 font-semibold text-blue-900">Password</label>
            <input
              type="password"
              className="w-full border border-gray-300 px-3 py-2 rounded focus:outline-none focus:ring focus:border-blue-500"
              placeholder="Enter Password"
            />
          </div>

          <button className="w-full bg-blue-900 text-white py-2 rounded hover:bg-black-900 font-sans font-bold">
            Login
          </button>

          <div className="text-sm text-center mt-4 mr-9">
            Don’t have an account? <a href="/signup" className="text-blue-600 hover:underline ml-0 font-semibold">Sign up</a>
            <div className="flex gap-20 ml-5 mt-3">
           <p className="text-blue-600 hover:underline ml-0"> Forgot Password</p> 
           <p>Remember Me <input type="checkbox"></input></p>
           </div>
          </div>
        </form>
      </div>
    </div>
  );
}
