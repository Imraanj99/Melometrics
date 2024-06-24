function TestRouteChange(value) {
    // Construct the new URL path
    const newPath = `/test/top_artists/${value}`;
    // Change the window's location
    window.location.pathname = newPath;
}