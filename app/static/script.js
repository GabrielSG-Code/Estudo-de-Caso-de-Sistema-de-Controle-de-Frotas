document.addEventListener('DOMContentLoaded', function(){
    const modalBody = document.getElementById('conteudoModal');

    //Quando qualquer botão de "detalhes" for clicado

    document.querySelectorAll('.btn-detalhes').forEach(button => {
        button.addEventListener('click', function(){
            const placa = this.getAttribute('data-placa');

            //Busca os dados na rota que foi criada via api
            fetch(`/api/veiculo/${placa}`)
            .then(response => response.json())
            .then(data => {
                //Preencher o modal com as informações do banco
                modalBody.innerHTML = `
                <p><strong>Model: </strong>${data.modelo}</p> 
                <p><strong>Placa: </strong>${data.placa}</p>
                <p><strong>Marca: </strong>${data.marca}</p>
                <p><strong>Ano: </strong>${data.ano}</p>
                <p><strong>Combustível: </strong>${data.combustivel}</p>
                <p><strong>Km Atual: </strong>${data.Km_atual}</p>
                <p><strong>Km da Última Troca de Óleo: </strong>${data.Km_UltimaTrocaOleo}</p>
                <p><strong>Km da Última Revisão: </strong>${data.Km_UltimaRevisao}</p>
                <p><strong>Data da Última Revisão: </strong>${data.Data_ultimaRevisao}</p>
                <p><strong>Status: </strong>${data.status}</p>
                `;
            })
            .catch(error => {
                modalBody.innerHTML = '<p class="text.danger">Erro ao carrega os dados da frota.</p>';
                console.error('Erro:', error);
            });
        });
    });
});
