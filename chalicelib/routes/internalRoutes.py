# Add all routes that are from this router/model/controller
def addRoutes(app):

    @app.route('/healthy')
    def healthy():
        return {'healthy': True}
