document.addEventListener("DOMContentLoaded", () => {
    
    // 1. Forum Reply (fetch POST)
    const replyForm = document.getElementById("reply-form");
    if (replyForm) {
        replyForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const body = document.getElementById("reply-body").value;
            const threadId = document.getElementById("thread-id").value;

            const res = await fetch(`/forum/${threadId}/reply`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ body })
            });

            if (res.ok) {
                const data = await res.json();
                // append new reply card to DOM
                const card = document.createElement("div");
                card.className = "reply-card card";
                
                // Format date as local string
                const dateStr = new Date(data.created_at).toLocaleString();
                
                card.innerHTML = `
                    <div class="flex justify-between mb-sm">
                        <p class="reply-author">${data.author}</p>
                        <p class="reply-date">${dateStr}</p>
                    </div>
                    <p>${data.body}</p>
                `;
                document.getElementById("replies-container").prepend(card);
                document.getElementById("reply-body").value = "";
            } else {
                alert("Failed to submit reply. Please make sure you are logged in.");
            }
        });
    }

    // 2. Domain Filter (live, client-side)
    const filterPills = document.querySelectorAll(".filter-pill");
    if (filterPills.length > 0) {
        filterPills.forEach(pill => {
            pill.addEventListener("click", () => {
                document.querySelectorAll(".filter-pill").forEach(p => p.classList.remove("active"));
                pill.classList.add("active");
                const domain = pill.dataset.domain;
                document.querySelectorAll(".mentor-card").forEach(card => {
                    const cardDomain = card.dataset.domain || "";
                    card.style.display = (domain === "all" || cardDomain.includes(domain)) ? "block" : "none";
                });
            });
        });
    }

    // 3. Booking Status Update (fetch PATCH)
    const statusBtns = document.querySelectorAll(".status-btn");
    if (statusBtns.length > 0) {
        statusBtns.forEach(btn => {
            btn.addEventListener("click", async () => {
                const bookingId = btn.dataset.id;
                const status = btn.dataset.status;
                const res = await fetch(`/booking/${bookingId}/status`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ status })
                });
                
                if (res.ok) {
                    const badge = document.querySelector(`#booking-${bookingId} .status-badge`);
                    if (badge) {
                        badge.textContent = status;
                        badge.className = `status-badge status-${status}`;
                    }
                    
                    // Remove the action buttons
                    const actionsContainer = btn.parentElement;
                    if (actionsContainer && actionsContainer.classList.contains('booking-actions')) {
                        actionsContainer.remove();
                    }
                } else {
                    alert("Failed to update status.");
                }
            });
        });
    }

    // Additional: Dashboard Tabs
    const tabBtns = document.querySelectorAll(".tab-btn");
    if (tabBtns.length > 0) {
        tabBtns.forEach(btn => {
            btn.addEventListener("click", () => {
                // Remove active class from all tabs
                document.querySelectorAll(".tab-btn").forEach(t => t.classList.remove("active"));
                document.querySelectorAll(".tab-content").forEach(c => c.classList.remove("active"));
                
                // Add active class to clicked tab
                btn.classList.add("active");
                const targetId = btn.dataset.target;
                document.getElementById(targetId).classList.add("active");
            });
        });
    }
});
