from flask_restful import Resource, reqparse, ResponseBase
from model.tipo_usuario import TipoUsuarioModel

argumentos = reqparse.RequestParser()
argumentos.add_argument('descricao', type=str, required=True, help="Campo 'descricao' não pode ser nulo.")

class TipoUsuarios(Resource):

    def get(self):

        tipo_usuarios = []
        tipos = TipoUsuarioModel.read_tipos()

        if tipos:

            for tipo in tipos:

                tipo_usuarios.append(tipo.json())

            return {'message': tipo_usuarios}, 200
            
        return {'message': 'TipoUsuarios não encontrados!'}, 404

    def post(self):

        dados = argumentos.parse_args()
        tipo_usuario = TipoUsuarioModel(**dados)
        
        if tipo_usuario.read_tipo(tipo_usuario.descricao):

            response = ResponseBase(response={'TipoUsuario já existe na base de dados!'}, 
                                    status=200, 
                                    headers={'location': '/tipousuario/'+ tipo_usuario.descricao})
            return response
        
        try:

            tipo_usuario.create_tipo()
            response = ResponseBase(response={'TipoUsuario criado com sucesso!'}, 
                                    status=201, 
                                    headers={'location': '/tipousuario/'+ tipo_usuario.descricao})
            return response

        except Exception as erro:
            response = ResponseBase(response={erro}, 
                                    status=500)
            return response

class TipoUsuario(Resource):

    def get(self, descricao):

        tipo_usuario = TipoUsuarioModel.read_tipo(descricao)

        if tipo_usuario:
            return {'message': tipo_usuario.json()}
        
        return {'message': 'TipoUsuario não encontrado!'}, 404

    def put(self, descricao):

        dados = argumentos.parse_args()
        tipo_usuario = TipoUsuarioModel.read_tipo(descricao)

        if tipo_usuario:

            tipo_usuario.update_tipo(**dados)
            tipo_usuario.create_tipo()

            return {'message': 'TipoUsuario editado com sucesso!'}

        return {'message': 'TipoUsuario não encontrado!'}, 404

    def delete(self, descricao):

        tipo_usuario = TipoUsuarioModel.read_tipo(descricao)

        if tipo_usuario:
            
            tipo_usuario.delete_tipo()
            return {'message': 'TipoUsuario deletado com sucesso!'}

        return {'message': 'TipoUsuario não encontrado!'}, 404
