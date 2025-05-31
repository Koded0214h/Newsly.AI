export default function Navbar() {
  return (
    <nav className="bg-green-700 text-black px-6 py-4 flex justify-between items-center shadow-md">
      <h1 className="text-2xl font-bold text-white font-heading"><i class="fa fa-newspaper-o" aria-hidden="true"></i> NewslyAI</h1>
      <ul className="flex space-x-6 text-lg font-bold">
        <li><a href="/feed" className=" text-white hover:underline ">Feed</a></li>
        <li><a href="#" className=" text-white hover:underline ">Explore</a></li>
        <li><a href="/profile2" className="text-white hover:underline">Profile</a></li>
        <li><a href="#" className="text-white hover:underline">Settings</a></li>
      </ul>
    </nav>
  );
}