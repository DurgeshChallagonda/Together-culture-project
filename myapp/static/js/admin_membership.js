document.addEventListener('DOMContentLoaded', function() {
    const filterButton = document.getElementById('filterButton');
    const searchButton = document.getElementById('searchButton');

    filterButton.addEventListener('click', function() {
        const membershipType = document.getElementById('membershipType').value;
        // filter logic
        console.log('Filtering by membership type:', membershipType);
    });

    searchButton.addEventListener('click', function() {
        const searchMember = document.getElementById('searchMember').value;
        // search logic
        console.log('Searching for member:', searchMember);
    });
});
