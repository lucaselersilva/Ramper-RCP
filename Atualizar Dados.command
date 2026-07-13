#!/bin/bash
# Duplo clique neste arquivo para extrair os dados mais recentes da API
# e abrir o dashboard atualizado. Pode ser usado a qualquer momento,
# fora do agendamento diário automático.

cd "$(dirname "$0")"

echo "======================================"
echo " Atualizando dados do Ramper Pipeline"
echo "======================================"
echo ""

python3 extract.py
STATUS=$?

echo ""
if [ $STATUS -eq 0 ]; then
  echo "Extração concluída com sucesso. Abrindo o dashboard..."
  open dashboard.html
else
  echo "A extração terminou com erro (veja acima). O dashboard não foi aberto automaticamente."
fi

echo ""
read -p "Pressione Enter para fechar esta janela..." _
