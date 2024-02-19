const searchField = document.getElementById('#searchField');
const tableOutput = document.getElementById('#tableOutput');
const appTable = document.getElementById('.appTable');
const paginationContainer = document.getElementById('#paginationContainer');  
tableOutput.innerHTML = '';
const noResult = document.getElementById('#noResult');

searchField.addEventListener('input', (e) => {
    const searchValue = e.target.value; 
    if(searchValue.trim().length > 0){
        paginationContainer.style.display = 'none';
        tbody.innerHTML = '';
        noResult.style.display = 'none';
        fetch('/search-income', {
            body: JSON.stringify({ searchText: searchValue }),
            method: 'POST',
        })
        .then((res) => res.json())
        .then((data) => {
            console.log('data', data);
            if(data.data.length === 0){
                noResult.style.display = 'block';
                tableOutput.innerHTML = '';
                appTable.style.display = 'none';
                paginationContainer.style.display = 'none';
            }else{
                appTable.style.display = 'block';
                noResult.style.display = 'none';
                tableOutput.innerHTML = data.data;
                paginationContainer.style.display = 'none';
            }
        });

    }
});