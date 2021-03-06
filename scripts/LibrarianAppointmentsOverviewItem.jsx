import * as React from 'react';

export default function LibrarianAppointmentsOverviewItem(props) {
  const { appointment } = props;

  function getDateString(timestamp) {
    const utcTs = new Date(timestamp);
    return utcTs.toLocaleDateString(
      'en-US',
      { hour: 'numeric', minute: '2-digit' },
    );
  }

  return (
    <div className="appointment">
      <p>
        Status:
        {appointment.status}
      </p>
      <p>
        Organizer:
        {' '}
        {appointment.organizer.name}
        {' '}
        (
        {appointment.organizer.ucid}
        )
      </p>

      <p>
        Attendees:
        {
                appointment.attendees
                  ? `\n\t${
                    appointment.attendees.map(
                      (attendee) => `${attendee.ucid}`,
                    ).join('\n\t')}`
                  : 'None'
            }
      </p>
      <p>
        Room Number:
        {appointment.room.room_number}
      </p>
      <p>
        Start Time:
        {getDateString(appointment.start_time)}
      </p>
      <p>
        End Time:
        {getDateString(appointment.end_time)}
      </p>
    </div>
  );
}
