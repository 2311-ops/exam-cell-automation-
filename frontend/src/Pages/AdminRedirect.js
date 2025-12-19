import { useEffect } from "react";

function AdminRedirect() {
  useEffect(() => {
    // Redirect to Django admin
    window.location.href = "http://127.0.0.1:8000/admin/";
  }, []);

  return null;
}

export default AdminRedirect;