export default function VerticalNavbar() {
  return (
    <div style={{ width: '200px', height: '100vh' }} className="bg-gray-800 text-white p-4 pb-6">
      <ul className="space-y-4 mb-6 text-1.5xl">
        <li className="hover:text-green-500 cursor-pointer"><i class="fa fa-user" aria-hidden="true"></i> Profile Overview</li>
        <li className="hover:text-green-500 cursor-pointer"><i class="fa fa-cog" aria-hidden="true"></i> Settings</li>
        <li className="hover:text-green-500 cursor-pointer"><i class="fa fa-star" aria-hidden="true"></i> Interests</li>
        <li><a href="/login" className="hover:text-green-500 cursor-pointer"><i class="fa fa-sign-out" aria-hidden="true"></i> Logout</a></li>
      </ul>
    </div>
    
  );
}