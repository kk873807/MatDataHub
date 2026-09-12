const fs = require('fs');

let content = fs.readFileSync('src/components/TopNav.tsx', 'utf8');

const oldFetch = `        fetch(\`\${API}/auth/me\`, {
          headers: { Authorization: \`Bearer \${token}\` }
        })
          .then(r => r.ok ? r.json() : null)
          .then(data => {
            if (data) { data.name = data.name || data.email; setUserInfo(data); }
          })
          .catch(() => {});`;

const newFetch = `        fetch(\`\${API}/auth/me\`, {
          headers: { Authorization: \`Bearer \${token}\` }
        })
          .then(async r => {
            if (r.ok) return r.json();
            if (r.status === 401) {
              const err = await r.json().catch(() => ({}));
              if (err.detail && err.detail.includes("another device")) {
                alert("Session expired. You have been logged in from another device or browser.");
              }
              localStorage.removeItem("token");
              setIsLoggedIn(false);
              setUserInfo(null);
              window.location.href = "/";
            }
            return null;
          })
          .then(data => {
            if (data) { data.name = data.name || data.email; setUserInfo(data); }
          })
          .catch(() => {});`;

content = content.replace(oldFetch, newFetch);
fs.writeFileSync('src/components/TopNav.tsx', content);
console.log('Fixed TopNav auth logic');
