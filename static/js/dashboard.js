const malesCount = {{ males_count }}
const femalesCount = {{ females_count }}

$(document).ready(function () {

    // Setup
    const labels = [
        gettext('January'),
        gettext('February'),
        gettext('March'),
        gettext('April'),
        gettext('May'),
        gettext('June'),
    ];
    const data = {
        labels: labels,
        datasets: [{
            label: gettext('Students'),
            backgroundColor: 'rgba(86, 224, 224, 0.5)',
            borderColor: 'rgb(86, 224, 224)',
            hoverBorderWidth: 3,
            data: [0, 10, 5, 2, 20, 30, 45]
        }, {
            label: gettext('Teachers'),
            backgroundColor: 'rgba(253, 174, 28, 0.5)',
            borderColor: 'rgb(253, 174, 28)',
            hoverBorderWidth: 3,
            data: [20, 0, 15, 4, 6, 4, 60],
        }, {
            label: gettext('Admins'),
            backgroundColor: 'rgba(203, 31, 255, 0.5)',
            borderColor: 'rgb(203, 31, 255)',
            hoverBorderWidth: 3,
            data: [85, 30, 34, 20, 20, 55, 45],
        }, {
            label: gettext('Stuffs'),
            backgroundColor: 'rgba(255, 19, 157, 0.5)',
            borderColor: 'rgb(255, 19, 157)',
            hoverBorderWidth: 3,
            data: [45, 75, 70, 80, 20, 30, 90],
        }]
    };

    var traffic = document.getElementById('traffic');
    var chart = new Chart(traffic, {
        type: 'line',
        data: data,
        options: {
            plugins: {
                title: {
                    display: true,
                    text: gettext('Website Traffic'),
                    padding: 15
                }
            }
        }
    });

    // Setup
    const labelsEnrollment = [
        '2016',
        '2017',
        '2018',
        '2019',
        '2020',
        '2021',
    ];
    const dataEnrollment = {
        labels: labelsEnrollment,
        datasets: [{
            label: gettext('Comp.S'),
            backgroundColor: 'rgba(86, 224, 224, 0.5)',
            borderColor: 'rgb(86, 224, 224)',
            hoverBorderWidth: 3,
            data: [0, 10, 5, 2, 20, 30, 45]
        }, {
            label: gettext('Architecture'),
            backgroundColor: 'rgba(253, 174, 28, 0.5)',
            borderColor: 'rgb(253, 174, 28)',
            hoverBorderWidth: 3,
            data: [20, 0, 15, 4, 6, 4, 60],
        }, {
            label: gettext('Civil Eng'),
            backgroundColor: 'rgba(203, 31, 255, 0.5)',
            borderColor: 'rgb(203, 31, 255)',
            hoverBorderWidth: 3,
            data: [85, 30, 34, 20, 20, 55, 45],
        }, {
            label: gettext('Accounting'),
            backgroundColor: 'rgba(255, 19, 157, 0.5)',
            borderColor: 'rgb(255, 19, 157)',
            hoverBorderWidth: 3,
            data: [45, 75, 70, 80, 20, 30, 90],
        }, {
            label: gettext('Business M.'),
            backgroundColor: 'rgba(0, 0, 0, 0.5)',
            borderColor: 'rgb(0, 0, 0)',
            hoverBorderWidth: 3,
            data: [15, 75, 45, 90, 60, 30, 90],
        }]
    };

    var enrollement = document.getElementById('enrollement');
    var chart = new Chart(enrollement, {
        type: 'bar',
        data: dataEnrollment,
        options: {
            plugins: {
                title: {
                    display: true,
                    text: gettext('Enrollment per course'),
                    padding: 20
                }
            }
        }
    });

    // Average grade setup
    const labelsGrade = [
        '2017',
        '2018',
        '2019',
        '2020',
        '2022',
    ];
    const dataGrade = {
        labels: labelsGrade,
        datasets: [{
            label: gettext("Comp sci."),
            backgroundColor: 'rgba(86, 224, 224, 0.5)',
            borderColor: 'rgb(86, 224, 224)',
            hoverBorderWidth: 3,
            data: [0, 10, 5, 2, 20, 30, 45]
        }, {
            label: gettext("Civil eng."),
            backgroundColor: 'rgba(253, 174, 28, 0.5)',
            borderColor: 'rgb(253, 174, 28)',
            hoverBorderWidth: 3,
            data: [20, 0, 15, 4, 6, 4, 60],
        }, {
            label: gettext("Architect."),
            backgroundColor: 'rgba(203, 31, 255, 0.5)',
            borderColor: 'rgb(203, 31, 255)',
            hoverBorderWidth: 3,
            data: [85, 30, 34, 20, 20, 55, 45],
        }, {
            label: gettext("Economics"),
            backgroundColor: 'rgba(255, 19, 157, 0.5)',
            borderColor: 'rgb(255, 19, 157)',
            hoverBorderWidth: 3,
            data: [45, 75, 70, 80, 20, 30, 90],
        }]
    };
    
    var students_grade = document.getElementById('students_grade');
    var chart = new Chart(students_grade, {
        type: 'bar',
        data: dataGrade,
        options: {
            plugins: {
                title: {
                    display: true,
                    text: gettext('Students average grade (performance)'),
                    padding: 20
                }
            }
        }
    });

    const dataGender = {
        labels: [
            gettext('Man'),
            gettext('Women')
        ],
        datasets: [{
            label: gettext("Students Gender Dataset"),
            data: [malesCount, femalesCount],
            backgroundColor: [
            'rgb(255, 99, 132)',
            'rgb(54, 162, 235)'
            ],
            hoverOffset: 4
        }]
    };

    var gender = document.getElementById('gender');
    var chart = new Chart(gender, {
        type: 'pie',
        data: dataGender,
        options: {
            plugins: {
                title: {
                    display: true,
                    text: gettext('Students Gender'),
                    padding: 20
                }
            }
        }
    });

    const dataQualification = {
        labels: [
            gettext('PHD'),
            gettext('Masters'),
            gettext('BSc degree')
        ],
        datasets: [{
            label: gettext("Lecturer Qualifications Dataset"),
            data: [24, 30, 26],
            backgroundColor: [
            'rgb(255, 99, 132)',
            'rgb(255, 193, 7)',
            'rgb(54, 162, 235)'
            ],
            hoverOffset: 4
        }]
    };
    var ethnicity = document.getElementById('ethnicity');
    var chart = new Chart(ethnicity, {
        type: 'pie',
        data: dataQualification,
        options: {
            plugins: {
                title: {
                    display: true,
                    text: gettext('Lecturer qualifications'),
                    padding: 20
                }
            }
        }
    });

    const dataLevels = {
        labels: [
            gettext('PHD'),
            gettext('Masters'),
            gettext('BSc degree')
        ],
        datasets: [{
            label: gettext("Students level"),
            data: [14, 30, 56],
            backgroundColor: [
            'rgb(255, 99, 132)',
            'rgb(255, 193, 7)',
            'rgb(54, 162, 235)'
            ],
            hoverOffset: 4
        }]
    };
    var language = document.getElementById('language');
    var chart = new Chart(language, {
        type: 'pie',
        data: dataLevels,
        options: {
            plugins: {
                title: {
                    display: true,
                    text: gettext('Student levels'),
                    padding: 20
                }
            }
        }
    });
})
