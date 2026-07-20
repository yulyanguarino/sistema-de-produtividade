CREATE TABLE IF NOT EXISTS colaboradores (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    ativo BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS operacoes (
    id SERIAL PRIMARY KEY,
    data DATE NOT NULL,
    pedido VARCHAR(50) NOT NULL,
    separador_id INTEGER NOT NULL REFERENCES colaboradores(id),
    qtd_itens_separados INTEGER NOT NULL CHECK (qtd_itens_separados >= 0),
    conferente_id INTEGER NOT NULL REFERENCES colaboradores(id),
    qtd_itens_conferidos INTEGER NOT NULL CHECK (qtd_itens_conferidos >= 0)
);

CREATE INDEX IF NOT EXISTS ix_operacoes_data ON operacoes(data);
CREATE INDEX IF NOT EXISTS ix_operacoes_separador_id ON operacoes(separador_id);
CREATE INDEX IF NOT EXISTS ix_operacoes_conferente_id ON operacoes(conferente_id);
