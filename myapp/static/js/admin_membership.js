document.addEventListener('DOMContentLoaded', function() {
    const filterButton = document.getElementById('filterButton');
    const searchButton = document.getElementById('searchButton');

    filterButton.addEventListener('click', function() {
        const membershipType = document.getElementById('membershipType').value;
        // Implement the filter logic here
        console.log('Filtering by membership type:', membershipType);
    });

    searchButton.addEventListener('click', function() {
        const searchMember = document.getElementById('searchMember').value;
        // Implement the search logic here
        console.log('Searching for member:', searchMember);
    });
});
