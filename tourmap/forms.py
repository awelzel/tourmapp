from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TextAreaField, BooleanField, SelectField
from wtforms.validators import DataRequired, Optional


class TourForm(FlaskForm):

    tour_exists_errors = ["A tour with this name already exists."]

    name = StringField(
        label="Name",
        render_kw={"placeholder": "Name"},
        validators=[DataRequired()],
        filters=[lambda data: data.strip() if data else data]  # Strip whitespace!
    )
    description = TextAreaField(
        label="Description",
        render_kw={"placeholder": "Optional description"},
        validators=[Optional()]
    )
    public = BooleanField(
        label="Public",
        render_kw={"placeholder": "Optional description"},
        false_values=["no", "false", "0"],
        default="no",
        validators=[Optional()]
    )
    start_date = DateField(
        label="Start Date",
        render_kw={"placeholder": "Optional start date"},
        validators=[Optional()]
    )
    end_date = DateField(
        label="End Date",
        render_kw={"placeholder": "Optional end date"},
        validators=[Optional()]
    )
    marker_positioning = SelectField(
        label="Marker Position",
        choices=[("end", "End"), ("middle", "Middle"), ("start", "Start")],
        default="end",
        validators=[Optional()]
    )
    marker_enable_clusters = BooleanField(
        label="Cluster Markers",
        false_values=["no", "false", "0"],
        default="no",
        validators=[Optional()]
    )
    polyline_color = SelectField(
        label="Line Color",
        choices=[
            ("red", "Red"),
            ("azure", "Azure"),
            ("gold", "Gold"),
            ("lightgreen", "Light Green"),
            ("blue", "Blue"),
            ("black", "Black"),
        ],
        validators=[Optional()]
    )

    def set_tour_exists(self):
        self.name.errors = self.tour_exists_errors
        self.errors["name"] = list(self.name.errors)
