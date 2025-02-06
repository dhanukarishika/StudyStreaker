// Function to update the badge colors and show the "Woohoo" message
function updateBadges() {
    const badges = [
      { id: "monday", color: "bg-primary-subtle" },
      { id: "tuesday", color: "bg-secondary-subtle" },
      { id: "wednesday", color: "bg-success-subtle" },
      { id: "thursday", color: "bg-danger-subtle" },
      { id: "friday", color: "bg-warning-subtle" },
      { id: "saturday", color: "bg-info-subtle" },
      { id: "sunday", color: "bg-light-subtle" }
    ];
  
    // Get the current date and time
    const currentTime = new Date().getTime();
  
    badges.forEach((badge, index) => {
      const badgeElement = document.getElementById(badge.id);
      const lastUpdatedTime = localStorage.getItem(badge.id); // Retrieve last updated time from localStorage
  
      // If the badge was last updated more than 24 hours ago, update it
      if (!lastUpdatedTime || currentTime - lastUpdatedTime >= 10) { // 24 hours = 86400000 ms
        // Change badge color to white with smooth transition
        badgeElement.classList.add("updated"); 
        badgeElement.style.transition = "all 0.3s ease-in-out";
  
        // Save the current time as the last updated time for this badge
        localStorage.setItem(badge.id, currentTime);
      }
    });
  
    // Check if all badges have been updated after 24 hours
    const allUpdated = badges.every(badge => {
      const lastUpdatedTime = localStorage.getItem(badge.id);
      return lastUpdatedTime && currentTime - lastUpdatedTime >= 10;
    });
  
    // If all badges are updated, display the "Woohoo" message with an animation
    if (allUpdated) {
      document.getElementById("message").style.display = "block";
      document.getElementById("message").classList.add("showMessage");
    }
  }
  
  // Run the updateBadges function when the page loads
  window.onload = updateBadges;
  
  // Add event listeners to badges for interactive hover effects
  document.querySelectorAll('.badge').forEach(badge => {
    badge.addEventListener('mouseover', function() {
      this.style.transform = 'scale(1.1)';
      this.style.transition = 'transform 0.2s';
    });
  
    badge.addEventListener('mouseout', function() {
      this.style.transform = 'scale(1)';
      this.style.transition = 'transform 0.2s';
    });
  });