# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
FROM python:3.9.0

WORKDIR /src

ENV FLASK_APP=flight_club
ENV FLASK_RUN_HOST=0.0.0.0

RUN apt-get update && apt-get install -y netcat

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["/src/entrypoint.sh"]
