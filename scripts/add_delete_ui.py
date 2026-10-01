import re

path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\next-frontend\src\app\admin\page.tsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

bad_block = '''  const handleBlockUser = async (userId: number) => {
    if (!confirm("Are you sure you want to block this user?")) return;
    try {
      const res = await fetch(`${API}/admin/users/${userId}/block`, {
        method: "POST", headers: { "Authorization": `Bearer ${localStorage.getItem("token")}` }
      });
      if (res.ok) {
        alert("User blocked successfully.");
        fetchAdminData(localStorage.getItem("token") || "");
      }
    } catch (err) {
      alert("Network error");
    }
  };'''

good_block = '''  const handleBlockUser = async (userId: number) => {
    if (!confirm("Are you sure you want to block this user?")) return;
    try {
      const res = await fetch(`${API}/admin/users/${userId}/block`, {
        method: "POST", headers: { "Authorization": `Bearer ${localStorage.getItem("token")}` }
      });
      if (res.ok) {
        alert("User blocked successfully.");
        fetchAdminData(localStorage.getItem("token") || "");
      }
    } catch (err) {
      alert("Network error");
    }
  };

  const handleDeleteUser = async (userId: number) => {
    if (!confirm("WARNING: This will permanently delete the user's account and all their data. Are you sure?")) return;
    try {
      const res = await fetch(`${API}/admin/users/${userId}`, {
        method: "DELETE", headers: { "Authorization": `Bearer ${localStorage.getItem("token")}` }
      });
      if (res.ok) {
        alert("User permanently deleted.");
        fetchAdminData(localStorage.getItem("token") || "");
      } else {
        alert("Failed to delete user.");
      }
    } catch (err) {
      alert("Network error");
    }
  };'''

content = content.replace(bad_block, good_block)

bad_ui = '''                            {fb.user_id && (
                              <button onClick={() => handleBlockUser(fb.user_id)} className="block text-red-500 hover:underline mt-1">Block User</button>
                            )}'''

good_ui = '''                            {fb.user_id && (
                              <div className="flex gap-3 mt-1">
                                <button onClick={() => handleBlockUser(fb.user_id)} className="text-orange-500 hover:underline">Block User</button>
                                <button onClick={() => handleDeleteUser(fb.user_id)} className="text-red-600 font-semibold hover:underline">Delete Account</button>
                              </div>
                            )}'''

content = content.replace(bad_ui, good_ui)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Added handleDeleteUser to frontend")
