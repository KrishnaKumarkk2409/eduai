// Handle the theme toggle functionality
document.querySelector('.switch input').addEventListener('change', (e) => {
    if (e.target.checked) {
      document.body.classList.add('dark-theme');
    } else {
      document.body.classList.remove('dark-theme');
    }
  });
  
  // Sidebar toggle functionality if needed
  document.querySelector('.sidebar-toggle').addEventListener('click', () => {
    const sidebar = document.querySelector('.sidebar');
    sidebar.classList.toggle('active'); // This will toggle visibility for the sidebar
  });
  