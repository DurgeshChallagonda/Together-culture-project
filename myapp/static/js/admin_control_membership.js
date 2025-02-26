document.addEventListener('DOMContentLoaded', function() {
    const pendingApplications = [
        { name: 'John Doe', email: 'john.doe@example.com', interests: 'Art, Music' },
        { name: 'Jane Smith', email: 'jane.smith@example.com', interests: 'Technology, Science' }
        // Add more pending applications as needed
    ];

    const tbody = document.querySelector('.pending-applications tbody');

    pendingApplications.forEach(application => {
        const row = document.createElement('tr');

        const nameCell = document.createElement('td');
        nameCell.textContent = application.name;
        row.appendChild(nameCell);

        const emailCell = document.createElement('td');
        emailCell.textContent = application.email;
        row.appendChild(emailCell);

        const interestsCell = document.createElement('td');
        interestsCell.textContent = application.interests;
        row.appendChild(interestsCell);

        const actionsCell = document.createElement('td');
        const approveButton = document.createElement('button');
        approveButton.textContent = 'Approve';
        approveButton.classList.add('btn', 'btn-success');
        actionsCell.appendChild(approveButton);

        const denyButton = document.createElement('button');
        denyButton.textContent = 'Deny';
        denyButton.classList.add('btn', 'btn-danger');
        actionsCell.appendChild(denyButton);

        row.appendChild(actionsCell);

        tbody.appendChild(row);
    });
});
