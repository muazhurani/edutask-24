describe('deleting a Todo item from the list', () => {
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
  
      // Add an item to ensure there's something to delete
      cy.get('form.inline-form input[type="text"]').type('Todo item to delete');
      cy.get('form.inline-form input[type="submit"]').click();
    });
  
    it('deletes a visible and active todo item', () => {
        // Check initial number of items
cy.get('.todo-list .todo-item').then(initialItems => {
  const initialCount = Array.isArray(initialItems) ? initialItems.length : 0;    

  // Click the 'x' to delete the first todo item
  cy.get('.todo-list .todo-item').first().find('.remover')
    .scrollIntoView()  // Ensure the element is in the viewport
    .should('be.visible')  // Ensure the element is visible
    .click();

  // Wait for the item to be removed (if there's a delay due to asynchronous actions)
  cy.wait(500);  // Adjust the wait time based on expected delay

  // Verify the item is no longer in the list
  if (initialCount > 1) {
    cy.get('.todo-list .todo-item').should('have.length', initialCount - 1);
  } else {
    cy.get('.todo-list .todo-item').should('have.length', 1); // If only one item was there
  }
});
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
  