function changeRoute(value) {
    // Construct the new URL path
    const newPath = `/top_artists/${value}`;
    // Change the window's location
    window.location.pathname = newPath;
}