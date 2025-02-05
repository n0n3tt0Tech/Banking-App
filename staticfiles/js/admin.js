document.addEventListener("DOMContentLoaded", function () {
    function filterTable(inputId, tableId) {
        const searchInput = document.getElementById(inputId);
        const tableRows = document.querySelectorAll(`#${tableId} tr`);
        
        searchInput.addEventListener("input", function () {
            const searchValue = searchInput.value.toLowerCase();
            tableRows.forEach(row => {
                const usernameCell = row.querySelector("td:first-child");
                if (usernameCell) {
                    const username = usernameCell.textContent.toLowerCase();
                    row.style.display = username.includes(searchValue) ? "" : "none";
                }
            });
        });
    }

    filterTable("userDetailsSearch", "userDetailsTable");
    filterTable("manageUsersSearch", "manageUsersTable");
});
