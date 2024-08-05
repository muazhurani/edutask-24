describe('toggling Todo item state', () => {
  let uid;
  let name;

  before(function () {
    // Create a user for the test
    cy.fixture('user.json').then((user) => {
      cy.request({
        method: 'POST',
        url: 'http://localhost:5001/users/create',
        form: true,
        body: user
      }).then((res) => {
        uid = res.body._id.$oid;
        name = user.firstName + " " + user.lastName;
      });
    });
  });

  beforeEach(function () {
    // before each test log in the user, create a task and open the task in view mode
    cy.visit('http://localhost:3000')

    cy.get('h1')
      .should('contain.text', 'Login')

    cy.get('.inputwrapper #email')
      .type('mon.doe@gmail.com')

    cy.get('form')
      .submit()

    cy.get('h1')
      .should('contain.text', 'Your tasks, Mon Doe')

    cy.get('.inputwrapper #title')
      .type(`My tasks for today`)

    cy.get('.inputwrapper #url')
      .type('https://www.youtube.com/watch?v=O6P86uwfdR0&list=WL&index=23&t=6s')

    cy.get('form')
      .submit()

    cy.get('.container-element' )
      .should('contain.text', 'My tasks for today')

    cy.contains('My tasks for today')
      .click()
  });

  it('marks an active todo item as done', () => {
    // Assuming there's a checker with class 'unchecked' to toggle
    cy.get('.todo-list .todo-item .checker.unchecked').first()
      .click();

    // Check if it's now marked as done
    cy.get('.todo-list .todo-item').first()
      .should('have.class', 'done-overlay')
      .find('.checker')
      .should('have.class', 'checked');
  });

  it('re-activates a done todo item', () => {
    // Assuming there's a checker with class 'checked' to toggle
    cy.get('.todo-list .todo-item .checker.checked').first()
      .click();

    // Check if it's now active again
    cy.get('.todo-list .todo-item').first()
      .should('not.have.class', 'done-overlay')
      .find('.checker')
      .should('have.class', 'unchecked');
  });


  after(function () {
    // Delete the user after tests
    cy.request({
      method: 'DELETE',
      url: `http://localhost:5001/users/${uid}`
    }).then((res) => {
      cy.log(res.body);
    });
  });
});
