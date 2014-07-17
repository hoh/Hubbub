{div, span} = React.DOM
{h1, h2, h3, h4} = React.DOM
{a, button} = React.DOM
{b, br} = React.DOM
{form, label, input} = React.DOM


Friend = React.createClass
    getInitialState: ->
        return {
            alias: @props.alias,
            active: @props.active,
        }

    render: ->
        div {},
            div {className: 'friendslist_name inline', title: @props.id},
                @state.alias
            div {className: 'friendslist_status inline'},
                if @state.active == true
                    "Active"
                else
                    "Inactive"
            div {className: 'friendslist_switch inline'},
                if @state.active == true
                    button {className: 'btn-red', onClick: @stopDummies},
                        "Stop"
                else
                    button {className: 'btn-green', onClick: @startDummies},
                        "Start"

    startDummies: ->
        $.ajax({
            url: "/friends/" + @props.id
            dataType: 'json'
            type: 'POST'
            data: {active: @state.active}

            success: ((data) ->
                @setState({active: data.active})
            ).bind(this)

            error: ((xhr, status, err) ->
                console.error(this.props.url, status, err.toString());
            ).bind(this)
        });


    stopDummies: ->
        $.ajax({
            url: "/friends/" + @props.id
            dataType: 'json'
            type: 'POST'
            data: {active: @state.active}

            success: ((data) ->
                @setState({active: data.active})
            ).bind(this)

            error: ((xhr, status, err) ->
                console.error(this.props.url, status, err.toString());
            ).bind(this)
        });


FriendsList = React.createClass
    getInitialState: ->
        return {
            mode: 'view',
            name: @props.name,
            original_name: @props.name,
            friends: [],
        }

    componentWillMount: ->
        $.ajax({
            url: "/friends/list"
            dataType: 'json'
            type: 'GET'

            success: ((data) ->
                @setState({friends: data})
            ).bind(this)

            error: ((xhr, status, err) ->
                console.error(this.props.url, status, err.toString());
            ).bind(this)
        });

    render: ->
        div {},
            (
                Friend f for f in @state.friends
            )

React.initializeTouchEvents(true)
React.renderComponent (FriendsList {
    foo: 42,
    }), document.getElementById('friendslist')